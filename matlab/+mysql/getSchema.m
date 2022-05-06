function obj = getSchema
persistent schemaObject
if isempty(schemaObject)
    schemaObject = dj.Schema(dj.conn, 'mysql', 'mysql');
end
obj = schemaObject;
end
