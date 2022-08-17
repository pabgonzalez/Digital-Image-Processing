clear all;
close all;

f = imread('barbara.gif');
[ysize,xsize] = size(f);

%mov_pics = avifile('aliasing_pics.avi', 'fps', 10, 'compression', 'none');
%mov_specs = avifile('aliasing_specs.avi', 'fps', 10, 'compression', 'none');
mov_pics = VideoWriter('aliasing_pics.avi');
mov_specs = VideoWriter('aliasing_specs.avi');
open (mov_pics);
open (mov_specs);

for xshrink = 0:5:600
desiredxsize = xsize - xshrink;
scale_shrink = desiredxsize / xsize;
T = maketform('affine',[scale_shrink 0 0; 0 scale_shrink 0; 0 0 1]);
f2 = imtransform(f,T);
[currentysize, currentxsize] = size(f2);

scale_boost = xsize / currentxsize;
Tinv = maketform('affine',[scale_boost 0 0; 0 scale_boost 0; 0 0 1]);

f3 = imtransform(f2,Tinv,'size',[ysize xsize]);
Fd = fftshift(log(1+abs(fft2(f3))));

%imshow([f3/max(max(f3));Fd/max(max(Fd))]);
%imshow(f3);
xshrink
fr = im2frame(f3, gray(256));
Fdr = im2frame(uint8(256*Fd/max(max(Fd))), gray(256));


% mov_pics = addframe(mov_pics, fr);
% mov_specs = addframe(mov_specs, Fdr);

 writeVideo(mov_pics, fr);
 writeVideo(mov_specs, Fdr);




end
close(mov_pics);
close(mov_specs);