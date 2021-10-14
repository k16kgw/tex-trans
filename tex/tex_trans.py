import glob
import pathlib
import shutil
import re

def change_suffix(file_name, from_suffix, to_suffix):
    # ファイルの拡張子を得る
    sf = pathlib.PurePath(file_name).suffix
    
    # 変更対象かどうか判定する
    if sf == from_suffix:
        # ファイル名(拡張子除く)を得る
        st = pathlib.PurePath(file_name).stem

        # 変更後のファイル名を得る
        to_name = st + to_suffix

        # ファイル名を変更する
        shutil.copyfile(file_name, to_name)
    
    return to_name

def tex_trans(data_lines):
    
    # \begin{document} 以下を抽出
    data_lines = re.search(r'\\begin{document}[\s\S]*\\end{document}', data_lines).group()

    # 余計な空白を一つに変換
    data_lines = re.sub('[ ]+', ' ', data_lines)
    # 改行後の空白を削除
    data_lines = re.sub('\n'+'[ ]+', '\n', data_lines) 
    # 複数改行を一つの改行に変換
    data_lines = re.sub('[\n]+', '\n', data_lines)

    # 方程式の変換
    equations = re.findall(r'\\begin{equation}[\s\S]*?\\end{equation}', data_lines)
    for equation in equations:
        data_lines = data_lines.replace(equation, 'EQUATION')
    equations = re.findall(r'\\begin{equation\*}[\s\S]*?\\end{equation\*}', data_lines)
    for equation in equations:
        data_lines = data_lines.replace(equation, 'EQUATION')
    aligns = re.findall(r'\\begin{align}[\s\S]*?\\end{align}', data_lines)
    for align in aligns:
        data_lines = data_lines.replace(align, 'EQUATION')
    aligns = re.findall(r'\\begin{align\*}[\s\S]*?\\end{align\*}', data_lines)
    for align in aligns:
        data_lines = data_lines.replace(align, 'EQUATION')
    gathers = re.findall(r'\\begin{gather}[\s\S]*?\\end{gather}', data_lines)
    for gather in gathers:
        data_lines = data_lines.replace(gather, 'EQUATION')
    eqnarrays = re.findall(r'\\begin{eqnarray}[\s\S]*?\\end{eqnarray}', data_lines)
    for eqnarray in eqnarrays:
        data_lines = data_lines.replace(eqnarray, 'EQUATION')
    # コメントアウトの削除
    commentouts = re.findall(r'%.*(?=\n)', data_lines)
    for com in commentouts:
        data_lines = data_lines.replace(com, '')
    # 行頭にバックスラッシュのある行の削除
    functions = re.findall(r'(\n\\[\s\S]*?)(?=\n)', data_lines)
    for func in functions:
        data_lines = data_lines.replace(func, '')
    # 文中の数式の変換
    eqs = re.findall(r'\$[\s\S]*?\$', data_lines)
    for eq in eqs:
        data_lines = data_lines.replace(eq, 'EQ')

    data_lines = data_lines.lstrip(r'\begin{document}')
    data_lines = data_lines.rstrip(r'\end{document}')

    # 文中の改行を削除
    data_lines = re.sub(r'\n(?=[a-z])', ' ', data_lines)
    data_lines = re.sub(r'\n(?=[0123456789])', ' ', data_lines)
    data_lines = re.sub('[ ]+', ' ', data_lines)

    return data_lines

def main():
    file_name = glob.glob('*.tex')[0]
    file_name = change_suffix(file_name, '.tex', '.txt')

    with open(file_name, encoding='utf-8') as f:
        data_lines = f.read()

    data_lines = tex_trans(data_lines)

    # 同じファイル名で保存
    new_file_name = 'output.txt'
    with open(new_file_name, mode='w', encoding='utf-8') as f:
        f.write(data_lines)

if __name__ == '__main__':
    main()