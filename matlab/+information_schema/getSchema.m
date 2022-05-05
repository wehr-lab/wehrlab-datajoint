function obj = getSchema
persistent schemaObject
if isempty(schemaObject)
    schemaObject = dj.Schema(dj.conn, 'information_schema', 'information_schema');
end
obj = schemaObject;
end
