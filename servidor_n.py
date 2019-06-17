from logging import getLogger, Formatter, INFO, FileHandler
from os import remove, stat, path, walk, makedirs, scandir, sep, getcwd, chmod
from datetime import date, timedelta, datetime
from time import mktime, sleep
from stat import S_IWRITE
from shutil import move
import zipfile
import glob

'''
msg_error = '[ERRO] Diretorio invalido, tente novamente:\n'

days_old = str(input('Defina quantos dias os arquivos sem acessos devem ser movidos:\n'))
while not days_old.isdigit():
    days_old = str(input('[ERRO] Insira apenas em numeros validos:\n'))
days_old = int(days_old)

pasta_origem = str(input('Insira o diretorio atual dos arquivos:\n'))
while not path.isdir(pasta_origem):
    pasta_origem = str(input(msg_error))

previa = str(input('Deseja ter uma previa de quantos arquivos e MB serão movidos? [S/N]\n')).upper()
while True:
    if str(previa) in ('S', 'N'):
        break
    else:
        previa = str(input('[ERRO] Por favor responda apenas "S" ou "N".\n')).upper()
'''
days_old = 5
pasta_origem = r'C:\Users\bomdi\Documents'
previa = 'S'


def clean_path(pathh):
    pathh = pathh.replace('/', sep).replace('\\', sep)
    if sep == '\\' and '\\\\?\\' not in pathh:
        # fix for Windows 260 char limit
        relative_levels = len([directory for directory in pathh.split(sep) if directory == '..'])
        cwd = [directory for directory in getcwd().split(sep)] if ':' not in pathh else []
        pathh = '\\\\?\\' + sep.join(cwd[:len(cwd) - relative_levels] \
                                     + [directory for directory in pathh.split(sep) if directory != ''][
                                       relative_levels:])
    return pathh


def funcao():
    global previa

    def log(level, msg, tofile=True):
        if previa == 'N':
            print(msg)

            if tofile:
                if level == 0:
                    logger.info(msg)
                else:
                    logger.error(msg)

    if previa == 'N':
        '''
        logfile = str(input('Insira o diretorio para salvar o log:\n'))
        while not path.isdir(logfile):
            logfile = str(input(msg_error))
        '''
        logfile = r'C:\Users\bomdi\Desktop'
        logfile = logfile + '\log_servidor_n.log'
        logger = getLogger("cuarch")
        hdlr = FileHandler(logfile, mode='a', encoding=None, delay=False)
        hdlr.setFormatter(Formatter('%(asctime)s - %(levelname)s: %(message)s'))
        logger.addHandler(hdlr)
        logger.setLevel(INFO)
        log(0, "Iniciando...")
        log(0, "—")
        print('\nOPERAÇÃO INICIADA')
        sleep(1)

    def end(code):
        if previa == 'N':
            log(0, '—')
            log(0, f'Diretório origem: "{pasta_origem}"')
            log(0, f'Diretório destino: "{pasta_destino}"')
            log(0, f'Diretório compactados: "{pasta_compactados}"')
            print(f'Log salvo em "{logfile}"')
            log(0, '—')
            log(0, "Fim.")
            log(0, "-------------------------")

            exit(code)

    count = 0
    size = 0.0

    # define a data
    move_date = date.today() - timedelta(days=days_old)
    move_date = mktime(move_date.timetuple())

    file_py = path.basename(__file__)
    today = datetime.now()
    for root, dirs, files in walk(pasta_origem):
        lista = [r'N:\TI\SuporteN2'
                 'N:\Certidoes_Diretoria'
                 'N:\Diretoria_Secretaria'
                 'N:\Juridico_Cred_Imob_Brad_BB'
                 'N:\Financeiro',]
        excecao_flag = len([i for i in lista if root.find(i) == 0 and (
                root[len(i):len(i) + 1] == '\\' or root[len(i):len(i) + 1] == '')]) == 0
        if excecao_flag:
            for file in files:
                # remove esse script da lista
                if file_py in files:
                    files.remove(file_py)
                # identificando o arquivo
                file_full = clean_path(path.join(root, file))
                data_file = stat(file_full).st_atime
                # valida a data
                if data_file < move_date:
                    # define o tamanho do arquivo que será movido
                    size = size + (path.getsize(f'{clean_path(root)}\{file}') / (1024 * 1024.0))
                    # após as condições, move o arquivo
                    if previa == 'N':
                        # criacao variavel do novo diretorio
                        novo_diretorio = root.replace(pasta_origem, pasta_destino + today.strftime('\\%Y')
                                                      + today.strftime('\\%m.%d'))
                        # criar a pasta
                        try:
                            makedirs(clean_path(novo_diretorio))
                        except:
                            pass
                        destino = path.join(clean_path(novo_diretorio), file)
                        # se existir remove o arquivo
                        try:
                            remove(destino)
                        except:
                            pass
                        chmod(file_full, S_IWRITE)
                        move(file_full, path.join(clean_path(novo_diretorio), file))
                        # log do que foi transferido
                        log(0, 'Transferido    "..\\' + file + '"    para->    "..\\' + novo_diretorio + '".')
                    count = count + 1
    if previa == 'N':
        log(0, "—")
        log(0, "Transferências: " + str(count) + " arquivos, totalizando " + str(round(size, 2)) + "MB.")
        log(0, "—")
        print('\nCOMPACTAÇÃO INICIADA')
        for d in scandir(pasta_destino + today.strftime('\\%Y') + today.strftime('\\%m.%d')):
            fdir = clean_path(path.join(pasta_destino + today.strftime('\\%Y') + today.strftime('\\%m.%d'), d))
            dest = clean_path(pasta_compactados + today.strftime('\\%Y') + today.strftime('\\%m.%d') + '\\'
                              + path.basename(fdir))
            if not path.exists(dest):
                makedirs(dest)
            for c in glob.glob1(fdir, "**"):
                pzipar = clean_path(path.join(fdir, c))
                with zipfile.ZipFile(pzipar + '.zip', 'w', zipfile.ZIP_DEFLATED, allowZip64=True,
                                     compresslevel=7) as zf:
                    lendirpath = len(pzipar)
                    lendirpathc = len(fdir)
                    if path.isdir(pzipar):
                        for roots, dirs, filenames in walk(pzipar):
                            for name in filenames:
                                name = clean_path(path.join(roots, name))
                                zf.write(name, name[lendirpath:])
                    else:
                        zf.write(pzipar, pzipar[lendirpathc:])
                    zf.close()
                omzip = pzipar + '.zip'
                dmzip = path.basename(pzipar) + '.zip'
                move(path.join(omzip), path.join(dest, dmzip))
                log(0, 'Subdiretório "{}" compactado e movido para "{}".'.format(path.basename(pzipar), pzipar))
        end(0)
    # resultado da previsão dos arquivos
    print('=' * 30)
    print('Transferências previstas:')
    print(str(count), 'Arquivos — ', end='')
    print(str(round(size, 2)), 'MB')
    print('=' * 30, '\n')
    op = str(input('Continuar operação? [S/N]\n')).upper()
    while True:
        if str(op) in ('S', 'N'):
            break
        else:
            op = str(input('[ERRO] Por favor responda apenas "S" ou "N".\n')).upper()
    if op == 'N':
        print('\nFIM DA OPERAÇÃO')
        exit()
    else:
        previa = 'N'


if previa == 'S':
    print('\nCALCULANDO ARQUIVOS...')
    sleep(1)
    funcao()
'''
pasta_destino = str(input('Insira o diretorio de destino dos arquivos:\n'))
while not path.isdir(pasta_destino):
    pasta_destino = str(input(msg_error))

pasta_compactados = str(input('Insira o diretorio destino para compactar os arquivos depois de movidos:\n'))
while not path.isdir(pasta_compactados):
    pasta_compactados = str(input(msg_error))
'''
pasta_destino = r'C:\Users\bomdi\Desktop\eae'
pasta_compactados = r'C:\Users\bomdi\Desktop\comp'
funcao()
