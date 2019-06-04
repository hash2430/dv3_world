import numpy
# See if sp, bapd, f0 has equal frame length
bapd_filename = "/home/administrator/projects/merlin/egs/build_your_own_voice/s1/database/feats/bap/p225_001.bapd"
bap_filename = "/home/administrator/projects/merlin/egs/build_your_own_voice/s1/database/feats/bap/p225_001.bap"
sp_filename = "/home/administrator/projects/merlin/egs/build_your_own_voice/s1/database/feats/sp/p225_001.sp"
f0_filename = "/home/administrator/projects/merlin/egs/build_your_own_voice/s1/database/feats/f0/p225_001.f0"
f0a_filename = "/home/administrator/projects/merlin/egs/build_your_own_voice/s1/database/feats/f0/p225_001.f0a"
lf0_filename = "/home/administrator/projects/merlin/egs/build_your_own_voice/s1/database/feats/lf0/p225_001.lf0"
mgc_filename = "/home/administrator/projects/merlin/egs/build_your_own_voice/s1/database/feats/mgc/p225_001.mgc"
mel_path = '/home/administrator/projects/deepvoice3_world_converter/preprocess_output_debug/p225_001-mel.npy'
linear_path = '/home/administrator/projects/deepvoice3_world_converter/preprocess_output_debug/p225_001-spec.npy'

filenames = []
filenames.append(bapd_filename) #(822, 2)
filenames.append(bap_filename) #(822, 1)
filenames.append(sp_filename) #(822, 513)
filenames.append(f0_filename) #(822, 1)
filenames.append(f0a_filename) #(434, 1)
filenames.append(lf0_filename) #(411, 1)
filenames.append(mgc_filename) #(411, 60)

dimensions = []
dimensions.append(1)
dimensions.append(1)
dimensions.append(513)
dimensions.append(1)
dimensions.append(1)
dimensions.append(1)
dimensions.append(60)

dtype = []
dtype.append(numpy.float64)
dtype.append(numpy.float64)
dtype.append(numpy.float64)
dtype.append(numpy.float64)
dtype.append(numpy.float32)
dtype.append(numpy.float32)
dtype.append(numpy.float32)

features = []
for file, dim, dt in zip(filenames, dimensions, dtype):
    with open(file, 'rb') as f:
        feature = numpy.fromfile(f, dtype=dt)
        feature = numpy.reshape(feature, (-1, dim))
    features.append(feature)

dv3_file_names = []
dv3_file_names.append(mel_path)
dv3_file_names.append(linear_path)

mel_spec = numpy.load(mel_path)
linear_spec = numpy.load(linear_path)



print("hi")