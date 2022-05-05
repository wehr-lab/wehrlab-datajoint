function obj = getSchema
persistent schemaObject
if isempty(schemaObject)
    schemaObject = dj.Schema(dj.conn, 'my_subject', 'my_subject');
end
obj = schemaObject;
end
