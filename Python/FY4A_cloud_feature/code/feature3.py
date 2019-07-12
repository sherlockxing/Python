#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-py
import ftplib
import netCDF4 as nc
import cv2
import numpy as np
import math
import os
import shutil
import csv
import time
import sys

class FtpDownload():
    def ftpDownload(self,user,passwd):
        server = 'ftp.nsmc.org.cn'
        bufsize = 1024*8

        ftp = ftplib.FTP(server, user, passwd)
        remoteDir = ftp.nlst()
        numFile = len(remoteDir)
        for i in range(numFile):
            remotepath = remoteDir[i]
            # 本地存储路径按需更改
            localpath = remotepath
            fp = open(localpath, 'wb')  # 以写模式在本地打开文件
            ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)
            print(str(i)+'/'+str(numFile))
            print('download'+'  '+str(remoteDir[i]))
        ftp.close()

    def makedir(self,path):
        if not os.path.exists(path):
            os.makedirs(path)

    def divide_choose_dir(self,day):
        filepath = os.getcwd()+'/'
        choose_path = filepath+'file/hdf_file/'+day+'/'
        listDir = os.listdir(choose_path)
        lenListDir = len(listDir)
        for i in range(lenListDir):
            if listDir[i][30:33] == 'CLM':
                src = choose_path+listDir[i]
                dst = filepath+'file/clm_file/'+day+'/'
                self.makedir(dst)
                dst = filepath+'file/clm_file/'+day+'/'+listDir[i]
                shutil.move(src, dst)
                print('move  CLM  '+listDir[i])
            else:
                print('not found  '+listDir[i])

class Dataset():
	def mkdir(self, fn):
	  if not os.path.exists(fn):
		  os.makedirs(fn)

	def lmicsv2png(self, hdfpath, csvfn, pngpath, band, wide, limitgec):
		hdffn = os.listdir(hdfpath)
		#csvfn = csvpath+'lmi.csv'
		for fn_hdf in hdffn:
		  try:
			  data = nc.Dataset(hdfpath+fn_hdf, 'r')
			  if band<10:
				  channel = 'NOMChannel0'+str(band)
			  else:
				  channel = 'NOMChannel'+str(band)
			  nom = data.variables[channel][:].data
		  except:
			  print('read hdf error:'+fn_hdf)
		  else:
			  print('read:'+fn_hdf)
			  #for fn_csv in csvfn:
				  #if (int(fn_csv[0:10])+1) == int(fn_hdf[44:54]): 
			  lmi = open(csvfn, 'r')
			  lmidata = csv.reader(lmi)
			  #print(fn_csv)
			  header = next(lmidata)
			  for row in lmidata:
				  if (int(row[8][0:12])) == int(fn_hdf[44:56])+5:
					  x = int(row[4])-wide/2
					  y = int(row[5])-wide/2
					  #print(x, y)
					  lon = str(round(float(row[6]), 3))
					  lat = str(round(float(row[7]), 3))
					  gec = float(row[3])
					  gecstr = str(round(float(row[3]), 3))
					  day = row[8][0:8]
					  time = row[8][8:14]
					  pngdir = pngpath+'nom'+str(band)+'/'+'wide'+str(wide)+'/'+'gec'+str(limitgec)+'/'
					  self.mkdir(pngdir)
					  if (gec > limitgec and gec<(limitgec+5)):
						  pngfn = pngpath+'nom'+str(band)+'/'+'wide'+str(wide)+'/'+'gec'+str(limitgec)+'/'+time+'_'+lon+'_'+lat+'_'+gecstr+'.png'
						  pic = [[0 for i in range(wide)] for i in range(wide)]
						  for i in range(wide):
							  for j in range(wide):
								  if nom[int(x)+i][int(y)+j] == 65535:
									  pic[i][j] = 255
								  else:
									  pic[i][j] = int(nom[int(x)+i][int(y)+j]/17)
						  dst = np.array(pic, dtype=np.uint8)
						  pic_int = dst.reshape(1, wide*wide)
						  ByteArray = bytearray(pic_int)
						  flatNumpyArray = np.array(ByteArray, dtype=np.uint8)
						  grayImage = flatNumpyArray.reshape(wide, wide)
						  cv2.imwrite(pngfn, grayImage)
						  print('write:'+pngfn)
					  else:
						  pass
					
	def clm2csv(self, clmpath, csvpath, start_x, start_y, end_x, end_y, wide):
		clmdir = os.listdir(clmpath)
		len_clmdir = len(clmdir)

		#csvpath = self.csvpath
		self.mkdir(csvpath)
		csvlmi = csvpath+'wide'+str(wide)+'clm.csv'
		
		headers = ['pic_x', 'pic_y', 'wide', 'time']
		with open(csvlmi, 'w') as f:
					f_csv = csv.writer(f)
					f_csv.writerow(headers)

		#start_x = self.start_x
		#start_y = self.start_y
		#end_x = self.end_x
		#end_y = self.end_y
		for n in range(len_clmdir):
			try:
				fn = clmpath+clmdir[n]
				data = nc.Dataset(fn, 'r')  # 默认为读文件，此处 'r' 可省略
				cloud = data.variables['CLM'][:].data
			except:
				print('read clm error:'+clmdir[n])
				pass
			else:
				print(clmdir[n])
				time = clmdir[n][44:58]
				for x in range(int((end_x-start_x)/wide)):
						for y in range(int((end_y-start_y)/wide)):
							cloud_x = start_x+x*wide
							cloud_y = start_y+y*wide
							cloud_wide = cloud[cloud_x:cloud_x+wide,cloud_y:cloud_y+wide] 
							if np.mean(cloud_wide) < 1:
								row = [str(cloud_x),str(cloud_y),str(wide),time]
								print(row)
								with open(csvlmi, 'a') as f:
									f_csv = csv.writer(f)
									f_csv.writerow(row)
					#print(pic_x, pic_y, lon[i], center_lon, lat[i], center_lat, near)
					#rows.append([lon[i], lat[i], gec[i], pic_x, pic_y, center_lon, center_lat, time])           
		return 0

	def clmcsv2png(self, hdfpath, csvpath, png, band, wide):
		#hdfpath = self.hdfpath
		#csvpath = self.csvpath
		hdffn = os.listdir(hdfpath)
		csvfn = 'wide'+str(wide)+'clm.csv'
		for fn_hdf in hdffn:
			try:
				data = nc.Dataset(hdfpath+fn_hdf, 'r')
			except:
				print('read hdf error:'+fn_hdf)
			else:
				if band<10:
					channel = 'NOMChannel0'+str(band)
				else:
					channel = 'NOMChannel'+str(band)
				nom = data.variables[channel][:].data
				print('read:'+fn_hdf)
				#for fn_csv in csvfn:
					#if (int(fn_csv[0:10])+1) == int(fn_hdf[44:54]): 
				clm = open(csvpath+csvfn, 'r')
				clmdata = csv.reader(clm)
				#print(fn_csv)
				header = next(clmdata)
				for row in clmdata:
					if (int(row[3][0:10])) == int(fn_hdf[44:54]):
						x = int(row[0])
						y = int(row[1])
						#print(x, y)
						#lon = str(round(float(row[5]), 3))
						#lat = str(round(float(row[6]), 3))
						#gec = float(row[2])
						#gecstr = str(round(float(row[2]), 3))
						day = row[3][0:8]
						time = row[3][8:14]
						
						#if_start_lon_in = bool(float(row[5])>self.start_lon)
						#if_end_lon_in = bool(float(row[5])<self.end_lon)
						#if_start_lat_in = bool(float(row[6])<self.start_lat)
						#if_end_lat_in = bool(float(row[6])>self.end_lat)
						#is_in_region = bool(if_start_lon_in and if_start_lat_in and if_end_lon_in and if_end_lat_in)
						if   wide == int(row[2]):
							pngpath = png+'nom'+str(band)+'/'+'wide'+str(wide)+'/'+'gec0'+'/'
							self.mkdir(pngpath)
							pngfn = png+'nom'+str(band)+'/'+'wide'+str(wide)+'/'+'gec0'+'/'+time+'_'+str(x)+'_'+str(y)+'.png'
							pic = [[0 for i in range(wide)] for i in range(wide)]
							for i in range(wide):
								for j in range(wide):
									if nom[int(x)+i][int(y)+j] == 65535:
										pic[i][j] = 255
									else:
										pic[i][j] = int(nom[int(x)+i][int(y)+j]/17)
							dst = np.array(pic, dtype=np.uint8)
							pic_int = dst.reshape(1, wide*wide)
							ByteArray = bytearray(pic_int)
							flatNumpyArray = np.array(ByteArray, dtype=np.uint8)
							grayImage = flatNumpyArray.reshape(wide, wide)
							cv2.imwrite(pngfn, grayImage)
							print('write:'+pngfn)
						else:
							pass

class GLCM():
    # 定义最大灰度级数
    gray_level = 16

    def maxGrayLevel(self,img):
        max_gray_level = 0
        (height, width) = img.shape
        # print(height, width)
        for y in range(height):
            for x in range(width):
                if img[y][x] > max_gray_level:
                    max_gray_level = img[y][x]
        return max_gray_level + 1


    def getGlcm(self,input, d_x, d_y):
        srcdata = input.copy()
        ret = [[0.0 for i in range(self.gray_level)] for j in range(self.gray_level)]
        (height, width) = input.shape

        max_gray_level = self.maxGrayLevel(input)

        # 若灰度级数大于gray_level，则将图像的灰度级缩小至gray_level，减小灰度共生矩阵的大小
        if max_gray_level > self.gray_level:
            for j in range(height):
                for i in range(width):
                    srcdata[j][i] = srcdata[j][i] * self.gray_level / max_gray_level

        for j in range(height - d_y):
            for i in range(width - d_x):
                rows = srcdata[j][i]
                cols = srcdata[j + d_y][i + d_x]
                ret[rows][cols] += 1.0

        for i in range(self.gray_level):
            for j in range(self.gray_level):
                ret[i][j] /= float(height * width)

        return ret

    def feature_computer(self,p):
        Con = 0.0
        Eng = 0.0
        Asm = 0.0
        Idm = 0.0
        for i in range(self.gray_level):
            for j in range(self.gray_level):
                Con += (i - j) * (i - j) * p[i][j]
                Asm += p[i][j] * p[i][j]
                Idm += p[i][j] / (1 + (i - j) * (i - j))
                if p[i][j] > 0.0:
                    Eng += p[i][j] * math.log(p[i][j])
        return Asm, Con, -Eng, Idm


    def glcm_return(self, fn):
        img = cv2.imread(fn)
        try:
            img_shape = img.shape
        except:
            #print('imread error')
            return [0, 0, 0, 0]

        img = cv2.resize(img, (img_shape[1] // 2, img_shape[0] // 2), interpolation=cv2.INTER_CUBIC)

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        glcm_0 = self.getGlcm(img_gray, 1, 0)
        # glcm_1=getGlcm(src_gray, 0,1)
        # glcm_2=getGlcm(src_gray, 1,1)
        # glcm_3=getGlcm(src_gray, -1,1)

        asm, con, eng, idm = self.feature_computer(glcm_0)
        row = [asm, con, eng, idm]
        return row

    def mkdir(self, fn):
        if not os.path.exists(fn):
            os.makedirs(fn)

    def calGLCM(self, pngpath, csvname):
        listDir = os.listdir(pngpath)
        lenListDir = len(listDir)
        headers = ['asm', 'con', 'eng', 'idm']
        rows = []
        for i in range(lenListDir):
            fn = pngpath+listDir[i]
            row = self.glcm_return(fn)
            print(str(i)+'/'+str(lenListDir)+':')
            print(row)
            rows.append(row)
            #print('ASM='+str(asm), 'CON='+str(con), 'ENT='+str(eng), 'IDM='+str(idm))
        #day = '20190420/'
        #csvpath = os.getcwd()+'/'+'file/dataset/'+day+'/'+'csv/' 
        #csvLMI = csvpath+csvname+'.csv'
        #self.mkdir(csvpath)
        with open(csvname, 'w') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(headers)
            f_csv.writerows(rows)
            #print(rows)
            #print('yes')

