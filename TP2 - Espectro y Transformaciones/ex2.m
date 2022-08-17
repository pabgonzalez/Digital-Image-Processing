clear all;
close all;
h=[0 1/6 0 ; 1/6 1/3 1/6 ; 0 1/6 0 ];

h = h/sum(h(:));
h = fspecial('unsharp');
%h = fspecial('disk');

b=imread('barbara.gif'); 
imshow(b);

h1=imfilter(b,h);    %make conv with the filter ==> 

figure
imshow(h1);


