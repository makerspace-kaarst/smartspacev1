import os


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
    path = basepath + path
    try:
        os.mkdir('/'.join(path.split('/')[:-1]))
    except FileExistsError:
        pass
    with open(path,'w') as f:
        f.write(text)


def delete_tmp(path, basepath):
    os.remove(basepath + path)


file_data = file_analysis()
generate_prebuild_report(file_data)
for p in file_data[1]:
    file_missing(p,'../content/deutsch/')

for p in file_data[2]:
    file_missing(p,'../content/english/')
print('\n'*3)
print('--------  Building Page  --------')
build_page()
print()
for p in file_data[1]:
    delete_tmp(p,'../content/deutsch/')

for p in file_data[2]:
    delete_tmp(p,'../content/english/')