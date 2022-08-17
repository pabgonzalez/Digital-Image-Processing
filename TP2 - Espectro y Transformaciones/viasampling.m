%%%Via sampling theory
 

clear all;
close all;

m=2;
f1 = imread('barbara.gif');
f1=f1(1:500,1:500);
f2=downsampling(f1,m,'FILTER_OFF');
%f2=downsampling(f1,m,'FILTER_ON');
f3=upsampling(f2,m);
figure; imshow(f1,[0 255]);
figure; imshow(f2,[0 255]);
figure; imshow(f3,[0 255]);