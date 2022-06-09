function obj = getSchema
persistent schemaObject
if isempty(schemaObject)
    schemaObject = dj.Schema(dj.conn, 'probe', 'probe');
end
obj = schemaObject;
end
