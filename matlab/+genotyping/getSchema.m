function obj = getSchema
persistent schemaObject
if isempty(schemaObject)
    schemaObject = dj.Schema(dj.conn, 'genotyping', 'genotyping');
end
obj = schemaObject;
end
