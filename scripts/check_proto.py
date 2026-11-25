"""Compare the compiled schema with the checked-in Python descriptor."""
from pathlib import Path
import subprocess
import tempfile

from google.protobuf.descriptor_pb2 import FileDescriptorProto, FileDescriptorSet
from pinba.pinba_pb2 import DESCRIPTOR

root = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as temporary:
    output = Path(temporary) / 'schema.pb'
    subprocess.run(['protoc', '-I', str(root / 'src/pinba'), '--descriptor_set_out=' + str(output),
                    str(root / 'src/pinba/pinba.proto')], check=True)
    descriptor_set = FileDescriptorSet.FromString(output.read_bytes())
    generated = FileDescriptorProto.FromString(DESCRIPTOR.serialized_pb)
    if len(descriptor_set.file) != 1:
        raise SystemExit('expected one schema descriptor')
    compiled = descriptor_set.file[0]
    # protoc adds derived json_name entries to descriptor sets but omits them
    # in generated bindings; these have no effect on the wire protocol.
    for descriptor in (compiled, generated):
        for message in descriptor.message_type:
            for field in message.field:
                field.ClearField('json_name')
    if compiled != generated:
        raise SystemExit('pinba.proto and generated bindings differ; regenerate with protoc')
