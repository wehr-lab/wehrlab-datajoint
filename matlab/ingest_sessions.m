%ingest session script
rootdir = '/mnt/ion-nas/Rig2/maddie';
d=dir(rootdir);
k=0;
for i=1:length(d)
    if strfind(d(i).name, '2022')
%         fprintf('\n%s', d(i).name)
        nb=loadNotebook(fullfile(rootdir, d(i).name));
        C=strsplit(d(i).name, '_mouse');
        session_datetime=C{1};
        k=k+1;
        stuff(k).subject= nb.mouseID;
        stuff(k).session_datetime=session_datetime  ;
    end
end

sess=session.getSchema();
insert(sess.v.Session, stuff)
