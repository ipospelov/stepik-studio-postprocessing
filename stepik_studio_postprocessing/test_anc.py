from stepik_studio_postprocessing.audio_processing.noise_cancellation.adaptive_cancellation import \
    AdaptiveNoiseCanceller
from stepik_studio_postprocessing.utils.descriptors.audio_file_descriptor import AudioFileDescriptor

anc = AdaptiveNoiseCanceller()
aux = AudioFileDescriptor('/Users/ivankirov/PycharmProjects/noise-cancellation/Presentation/2_aux_input.wav')
main = AudioFileDescriptor('/Users/ivankirov/PycharmProjects/noise-cancellation/Presentation/2_main_input.wav')
anc.process(main, aux, '/Users/ivankirov/PycharmProjects/noise-cancellation/Presentation/test_out.wav')
