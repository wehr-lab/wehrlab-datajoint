function obj = getSchema
persistent schemaObject
if isempty(schemaObject)
    schemaObject = dj.Schema(dj.conn, 'subject', 'subject');
end
obj = schemaObject;
end
