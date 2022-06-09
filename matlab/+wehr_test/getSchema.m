function obj = getSchema
persistent schemaObject
if isempty(schemaObject)
    schemaObject = dj.Schema(dj.conn, 'wehr_test', 'wehr_test');
end
obj = schemaObject;
end
