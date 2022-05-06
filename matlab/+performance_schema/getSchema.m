function obj = getSchema
persistent schemaObject
if isempty(schemaObject)
    schemaObject = dj.Schema(dj.conn, 'performance_schema', 'performance_schema');
end
obj = schemaObject;
end
