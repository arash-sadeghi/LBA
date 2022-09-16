clc; clear all; close all;
load sata.mat
x = -0.8:0.05:0.8-0.05;
y = 0.4:0.05:1.8-0.05;

mat = abs(mat);
% error_x,error_y,error_rot,dataFlag

er_x = mean(mat(:,:,3,:),4);
er_y = mean(mat(:,:,4,:),4);
er_t = sqrt(er_x.^2+er_y.^2);
% er_b = mean(mat(:,:,5,:),4);
% er_b = max(mat(:,:,5,:),[],4);
er_b = min(mat(:,:,5,:),[],4);

det  = mean(mat(:,:,6,:),4);

[xx,yy] = meshgrid(x,y);

% surf(xx,yy,er_t')
surf(xx,yy,er_b')
% surf(xx,yy,det')