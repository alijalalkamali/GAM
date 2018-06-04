def file_loader(filename, col=0):
    '''
    Read certain coloumn from text file.
    '''
    with open(filename) as fp:
        ret = fp.readlines()
        ret = [line.split()[col] for line in ret]
        return ret
    return None