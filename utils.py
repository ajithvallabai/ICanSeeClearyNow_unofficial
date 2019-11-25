import torch
from torch.autograd import Variable
from torchvision.utils import save_image

def sample_images(generator, test_dataloader, args, epoch, batches_done):
    """Saves a generated sample from the validation set"""
    imgs = next(iter(test_dataloader))
    real_A , real_B = imgs 
    real_A = Variable(real_A.cuda()); real_B = Variable(real_B.cuda())
    fake_B = generator(real_A)
    img_sample = torch.cat((real_A.data, fake_B.data, real_B.data), -2)
    save_image(img_sample, '%s-%s/%s/%s-%s.png' % (args.exp_name, args.dataset_name, args.img_result_dir, batches_done, epoch), nrow=5, normalize=False)



def print_network(net):
    num_params = 0
    for param in net.parameters():
        num_params += param.numel()
    print(net)
    print('Total number of parameters: %d' % num_params)



class LambdaLR():
    def __init__(self, epoch_num, epoch_start, decay_start_epoch):
        assert ((epoch_num - decay_start_epoch) > 0), "Decay must start before the training session ends!"
        self.epoch_num = epoch_num
        self.epoch_start = epoch_start
        self.decay_start_epoch = decay_start_epoch

    def step(self, epoch):
        return 1.0 - max(0, epoch + 1 + self.epoch_start - self.decay_start_epoch)/(self.epoch_num - self.decay_start_epoch)
