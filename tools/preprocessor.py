import os
import shutil

def list_files(path):
    return _list_files(path,'')


def _list_files(path, _relative):
    f = []
    dirnames = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        f.extend([_relative+x for x in filenames])
        break

    for dn in dirnames:
        f.extend(_list_files(path+'/'+dn,dn+'/'))
    return f


def file_analysis():
    de = list_files('../content/deutsch')
    en = list_files('../content/english')
    missing_in_en = list(set(de) - set(en))
    missing_in_de = list(set(en) - set(de))
    all_unique_files = list(set(en+de))
    return all_unique_files,missing_in_de,missing_in_en


def build_page():
    tmp = os.getcwd()
    os.chdir('..')
    os.system('hugo')
    os.chdir(tmp)


def generate_prebuild_report(report):
    print('--------  Content statistics  --------')
    print('Unique files [Ignores translations]: '+str(len(report[0])))

    print('files missing a german translation: '+str(len(report[1])))
    for item in report[1]: print('  '+item)
    if len(report[1]): print()

    print('files missing an english translation: '+str(len(report[2])))
    for item in report[2]: print('  '+item)
    if len(report[2]): print()


def file_missing(path, basepath):
    with open('static/missing_file_' + ('de' if 'deutsch' in basepath else 'en')+'.md','r') as f:
        text = f.read()
    final_path = basepath + path
    try:
        os.mkdir('/'.join(final_path.split('/')[:-1]))
    except FileExistsError:
        pass
    with open(final_path,'w') as f:
        f.write(text.replace('{path}','.'.join(path.split('.')[:-1])))


def delete_tmp(path, basepath):
    os.remove(basepath + path)


def title_of(file,lang):
    with open('../content/'+lang+'/'+file,'r') as f:
        title = f.readlines()[1].replace('title:','').strip()[1:-1]
    return title


def make_link(file,lang):
    base = f"""-
    name: "{ title_of(file,lang)}"
    url: "{('.'.join(file.split('.')[:-1])).split('/')[-1]}"
    bg_color: "#f2a71d"
    txt_color: "#f5f8fa"
    tags: ["text"]
"""
    print(base)
    return base

file_data = file_analysis()

with open('static/links.yml','r') as f:
    links = f.read()
for file in file_data[0]:
    try:
        links += make_link(file,'english')
    except FileNotFoundError:
        links += make_link(file,'deutsch')
with open('../data/links.yml','w') as f:
    f.write(links)

generate_prebuild_report(file_data)
for p in file_data[1]:
    file_missing(p,'../content/deutsch/')

for p in file_data[2]:
    file_missing(p,'../content/english/')

print('\n'*3)
folder = '../public'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))
build_page()


for p in file_data[1]:
    delete_tmp(p,'../content/deutsch/')

for p in file_data[2]:
    delete_tmp(p,'../content/english/')
