%just testing out connecting to datajoint database

%%
dj.version

fname = '~/.djcredentials.json'; 
fid = fopen(fname); 
raw = fread(fid,inf); 
str = char(raw'); 
fclose(fid); 
djcred = jsondecode(str);
setenv('DJ_HOST', djcred.host)
setenv('DJ_USER', djcred.user)
setenv('DJ_PASS', djcred.password)

%dj.config('databasePort', 3307)
dj.config('databaseUse_tls', false)
dj.config
conn=dj.conn()

%doesn't work? make sure the sql server is running
%    docker-compose up -d
%this either launches it or tells you it's up to date (already running)
%%

conn.query('show schemas')
dj.createSchema
%Enter database name >> subject
%create +subject folder

%note that "database" refers to the schema

%%
s=subject.getSchema()
s.v
s.v.Subject

%%
cd('/home/lab/git/wehrlab-datajoint/matlab')
