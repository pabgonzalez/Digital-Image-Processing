clear all;
close all;
f1 = imread('barbara.gif');
size(f1)
%f=ind2gray(f,gray(256));
f1=f1(1:500,1:500);

m=3; %downsampling factor 

%f2=imresize(f1,1/m,'nearest'); % Downsample to a 1/5th of the size no antialias


f2=imresize(f1,1/m,'bic'); % Downsample to a 1/5th of the size antialias

%h = fspecial('disk',1);
%h = fspecial('gaussian',[8 8],.8);

%f2=imfilter(f2,h);    %make conv with the filter ==> 



f3=imresize(f2,m); % Go back to original size
figure; imshow(f1);
figure; imshow(f2);
figure; imshow(f3);

%freqz2(h);
