function createSchemas(conn)
%inputs: conn datajoint db object returned by connect

schema_list=conn.query('show schemas');
for i=1:length(schema_list.Database)
    schema=schema_list.Database{i};
    [path, ~, ~]=fileparts(which(mfilename));
    dj.createSchema(schema, path, schema)
end