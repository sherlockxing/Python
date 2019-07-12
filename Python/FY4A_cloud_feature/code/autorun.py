import feature3 as fe
import gc
import time
import os

fp = input('input dir name:')
fy = fe.FtpDownload()
'''
codepath = os.getcwd()+'/'
fp = codepath+'file/'+'hdf_file/'+str(fp)
os.makedirs(fp)
os.chdir(fp)
print(os.getcwd())
user = input('input user:')
passwd = input('input passwd:')
user = str(user)
passwd  = str(passwd)
fy.ftpDownload(user,passwd) #下载hdf，clm
'''

#fy.divide_choose_dir(str(fp)) #clm分类

#nom = input('input nom:')
#nom = int(nom)

fp = ['20190401','20190402','20190403','20190404','20190405']
for fp in fp:
    day = str(fp)
    codepath = os.getcwd()+'/'
    hdfpath = codepath+'file/'+'hdf_file/'+day+'/'
    csvfn = codepath+'file/'+'hdf_file/'+'csv/sam'+day+'.csv'
    png = codepath+'file/dataset/'+day+'/'
    glcm = fe.GLCM()
    clmpath = codepath+'file/clm_file/'+day+'/'
    csvpath = codepath+'file/clm_file/'+day+'/'+'csv/'
    db = fe.Dataset()
    db.mkdir(png)
    
    start_x = 300
    start_y = 900
    end_x = 900
    end_y = 1900

    fy = fe.Dataset()
    for wide in [25,50]:
        fy.clm2csv(clmpath, csvpath, start_x, start_y, end_x, end_y, wide)
    for nom in [9,10,11,12,13,14]:
        for wide in [25,50]:
            fy.clmcsv2png(hdfpath, csvpath, png, nom, wide)
            gc.collect()
            time.sleep(5)

''' 
    for nom in [10]:
            for wide in [25,50]:
                        for gec in [5,10]:
                                        db.lmicsv2png(hdfpath,csvfn,png,nom,wide,gec)
                                                        gc.collect()
                                                                        time.sleep(10)
                                                                        '''
'''
    for nom in [10]:
        for wide in [25,50]:
            for gec in [0,10]:
                pngpath = png+'nom'+str(nom)+'/wide'+str(wide)+'/gec'+str(gec)+'/'
                csvname = 'nom'+str(nom)+'wide'+str(wide)+'gec'+str(gec)
                csvpath = os.getcwd()+'/'+'file/dataset/'+day+'/'+'csv/'
                glcm.mkdir(csvpath)
                csvLMI = csvpath+csvname+'.csv'
                glcm.calGLCM(pngpath, csvLMI)
'''
