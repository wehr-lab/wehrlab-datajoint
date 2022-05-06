function conn = connect()
%connect to wehrlab datajoint database

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