import numpy as np
from PIL import Image
import time

def compute_gradient(arr):
	# calculate gradients + convert them to polar form
	grady, gradx = np.gradient(arr, axis=(0,1))
	mags = np.hypot(grady, gradx)
	angles = np.arctan2(grady, gradx)

	# make angles range from [-pi/2,pi/2] to [0,180]
	angles = (angles * 180 / np.pi + 180) % 180

	if len(mags.shape) > 2:
		# get max magnitude among all channels for each pixel
		mxmag = np.argmax(mags, axis=2)
		yy, xx = np.ogrid[:mxmag.shape[0], :mxmag.shape[1]]
		angles = angles[yy, xx, mxmag]
		mags = mags[yy, xx, mxmag]

	return mags, angles

def make_histogram(mags, angles, bins):
	ysz, xsz = angles.shape
	binsz = 180 // bins
	hist = np.zeros(bins, dtype="float32")

	for i in range(ysz):
		for j in range(xsz):
			a, m = angles[i][j], mags[i][j]
			bin1 = int(a // binsz)
			bin2 = (bin1 + 1) % bins
			diff1 = (a - bin1 * binsz) / binsz
			diff2 = 1 - diff1

			hist[bin1] += diff1 * a
			hist[bin2] += diff2 * a

	return hist

def create_cells(mags, angles, cell_sz, bins):
	ysz, xsz = angles.shape
	hists = np.zeros((ysz//cell_sz+1, xsz//cell_sz+1, bins))

	for i in range(0, ysz, cell_sz):
		for j in range(0, xsz, cell_sz):
			cell_mags = mags[i:i+cell_sz, j:j+cell_sz]
			cell_angles = angles[i:i+cell_sz, j:j+cell_sz]
			hists[i//cell_sz][j//cell_sz] = make_histogram(cell_mags, cell_angles, bins)
	
	return hists

def normalize(hists):
	res = []
	ysz, xsz, bins = hists.shape

	for i in range(ysz-1):
		for j in range(xsz-1):
			cur = np.concatenate((
				hists[i][j],
				hists[i+1][j],
				hists[i][j+1],
				hists[i+1][j+1]
			))
			if np.linalg.norm(cur) != 0:
				cur = cur / np.linalg.norm(cur)
			res += [cur]

	return np.array(res).flatten()

def hog(im, bins=9, cell_sz=16):
	mags, angles = compute_gradient(im)
	hists = create_cells(mags, angles, cell_sz=cell_sz, bins=bins)
	desc = normalize(hists)
	return desc