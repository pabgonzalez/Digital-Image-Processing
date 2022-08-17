

clear all;
close all;
% Prepare image
f = zeros(30,30);
f(5:24,13:17) = 1;
imshow(f)
% Compute Fourier Transform
F = fft2(f,256,256);
F = fftshift(F); % Center FFT
% Measure the minimum and maximum value of the transform amplitude
min(min(abs(F))) % 0
max(max(abs(F))) % 100
figure; imshow(abs(F),[0,100]); colormap(jet); colorbar
figure; imshow(log(1+abs(F)),[0,3]); colormap(jet); colorbar
% What is the main difference between representing the amplitude and its logarithm?
% Look at the phases
figure; imshow(angle(F),[-pi,pi]); colormap(jet); colorbar
%* Try with other images
%f = imread('saturn.tif');
%f = ind2gray(f,gray(256));