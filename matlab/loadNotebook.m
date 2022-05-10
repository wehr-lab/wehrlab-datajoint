function nb = loadNotebook(BonsaiDir)
%load notebook file from ephys directory inside the BonsaiDir 
% and return as structure nb


EphysDir=dir(fullfile(BonsaiDir,'2022*')).name;
s=load(fullfile(BonsaiDir, EphysDir, 'notebook.mat'));
nb=s.nb;
