import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.modules.utils import _pair

from utils.utils_d3net import choose_layer_norm, choose_nonlinear

EPS = 1e-12

class D2BlockFixedDilation(nn.Module):
    def __init__(self, in_channels, growth_rate, kernel_size, dilation=1, norm=True, nonlinear='relu', depth=None, eps=EPS):
        """
        Args:
            in_channels <int>: # of input channels
            growth_rate <int> or <list<int>>: # of output channels
            kernel_size <int> or <tuple<int>>: Kernel size
            dilated <bool> or <list<bool>>: Applies dilated convolution.
            norm <bool> or <list<bool>>: Applies batch normalization.
            nonlinear <str> or <list<str>>: Applies nonlinear function.
            depth <int>: If `growth_rate` is given by list, len(growth_rate) must be equal to `depth`.
        """
        super().__init__()

        if type(growth_rate) is int:
            assert depth is not None, "Specify `depth`"
            growth_rate = [growth_rate] * depth
        elif type(growth_rate) is list:
            if depth is not None:
                assert depth == len(growth_rate), "`depth` is different from `len(growth_rate)`"
            depth = len(growth_rate)
        else:
            raise ValueError("Not support growth_rate={}".format(growth_rate))
        
        if type(norm) is bool:
            assert depth is not None, "Specify `depth`"
            norm = [norm] * depth
        elif type(norm) is list:
            if depth is not None:
                assert depth == len(norm), "`depth` is different from `len(norm)`"
            depth = len(norm)
        else:
            raise ValueError("Not support norm={}".format(norm))

        if type(nonlinear) is bool or type(nonlinear) is str:
            assert depth is not None, "Specify `depth`"
            nonlinear = [nonlinear] * depth
        elif type(nonlinear) is list:
            if depth is not None:
                assert depth == len(nonlinear), "`depth` is different from `len(nonlinear)`"
            depth = len(nonlinear)
        else:
            raise ValueError("Not support nonlinear={}".format(nonlinear))
        
        self.growth_rate = growth_rate
        self.depth = depth

        net = []
        _in_channels = in_channels

        for idx in range(depth):
            _out_channels = sum(growth_rate[idx:])
            conv_block = ConvBlock2d(_in_channels, _out_channels, kernel_size=kernel_size, stride=1, dilation=dilation, norm=norm[idx], nonlinear=nonlinear[idx], eps=eps)
            net.append(conv_block)
            _in_channels = growth_rate[idx]

        self.net = nn.ModuleList(net)
    
    def forward(self, input):
        """
        Args:
            input: (batch_size, in_channels, H, W)
        Returns:
            output: (batch_size, out_channels, H, W), where `out_channels` is determined by ... 
        """
        growth_rate, depth = self.growth_rate, self.depth

        x = input
        x_residual = 0

        for idx in range(depth):
            x = self.net[idx](x)
            x_residual = x_residual + x
            
            in_channels = growth_rate[idx]
            stacked_channels = sum(growth_rate[idx+1:])
            sections = [in_channels, stacked_channels]

            if idx != depth - 1:
                x, x_residual = torch.split(x_residual, sections, dim=1)
        
        output = x_residual

        return output

class D2Block(nn.Module):
    def __init__(self, in_channels, growth_rate, kernel_size, dilated=True, norm=True, nonlinear='relu', depth=None, eps=EPS):
        """
        Args:
            in_channels <int>: # of input channels
            growth_rate <int> or <list<int>>: # of output channels
            kernel_size <int> or <tuple<int>>: Kernel size
            dilated <bool> or <list<bool>>: Applies dilated convolution.
            norm <bool> or <list<bool>>: Applies batch normalization.
            nonlinear <str> or <list<str>>: Applies nonlinear function.
            depth <int>: If `growth_rate` is given by list, len(growth_rate) must be equal to `depth`.
        """
        super().__init__()

        if type(growth_rate) is int:
            assert depth is not None, "Specify `depth`"
            growth_rate = [growth_rate] * depth
        elif type(growth_rate) is list:
            if depth is not None:
                assert depth == len(growth_rate), "`depth` is different from `len(growth_rate)`"
            depth = len(growth_rate)
        else:
            raise ValueError("Not support growth_rate={}".format(growth_rate))
        
        if type(dilated) is bool:
            assert depth is not None, "Specify `depth`"
            dilated = [dilated] * depth
        elif type(dilated) is list:
            if depth is not None:
                assert depth == len(dilated), "`depth` is different from `len(dilated)`"
            depth = len(dilated)
        else:
            raise ValueError("Not support dilated={}".format(dilated))
        
        if type(norm) is bool:
            assert depth is not None, "Specify `depth`"
            norm = [norm] * depth
        elif type(norm) is list:
            if depth is not None:
                assert depth == len(norm), "`depth` is different from `len(norm)`"
            depth = len(norm)
        else:
            raise ValueError("Not support norm={}".format(norm))

        if type(nonlinear) is bool or type(nonlinear) is str:
            assert depth is not None, "Specify `depth`"
            nonlinear = [nonlinear] * depth
        elif type(nonlinear) is list:
            if depth is not None:
                assert depth == len(nonlinear), "`depth` is different from `len(nonlinear)`"
            depth = len(nonlinear)
        else:
            raise ValueError("Not support nonlinear={}".format(nonlinear))
        
        self.growth_rate = growth_rate
        self.depth = depth

        net = []
        _in_channels = in_channels

        for idx in range(depth):
            _out_channels = sum(growth_rate[idx:])
            if dilated[idx]:
                dilation = 2**idx
            else:
                dilation = 1
            conv_block = ConvBlock2d(_in_channels, _out_channels, kernel_size=kernel_size, stride=1, dilation=dilation, norm=norm[idx], nonlinear=nonlinear[idx], eps=eps)
            net.append(conv_block)
            _in_channels = growth_rate[idx]

        self.net = nn.ModuleList(net)
    
    def forward(self, input):
        """
        Args:
            input: (batch_size, in_channels, H, W)
        Returns:
            output: (batch_size, out_channels, H, W), where `out_channels` is determined by ... 
        """
        growth_rate, depth = self.growth_rate, self.depth

        x = input
        x_residual = 0

        for idx in range(depth):
            x = self.net[idx](x)
            x_residual = x_residual + x
            
            in_channels = growth_rate[idx]
            stacked_channels = sum(growth_rate[idx+1:])
            sections = [in_channels, stacked_channels]

            if idx != depth - 1:
                x, x_residual = torch.split(x_residual, sections, dim=1)
        
        output = x_residual

        return output

class ConvBlock2d(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, stride=1, dilation=1, norm=True, nonlinear='relu', eps=EPS):
        super().__init__()

        assert stride == 1, "`stride` is expected 1"

        self.kernel_size = _pair(kernel_size)
        self.dilation = _pair(dilation)

        self.norm = norm
        self.nonlinear = nonlinear

        if self.norm:
            if type(self.norm) is bool:
                name = 'BN'
            else:
                name = self.norm
            self.norm2d = choose_layer_norm(name, in_channels, n_dims=2, eps=eps)
        
        if self.nonlinear is not None:
            self.nonlinear2d = choose_nonlinear(self.nonlinear)
        
        self.conv2d = nn.Conv2d(in_channels, out_channels, kernel_size=kernel_size, stride=stride, dilation=dilation)

    def forward(self, input):
        """
        Args:
            input (batch_size, in_channels, H, W)
        Returns:
            output (batch_size, out_channels, H, W)
        """
        kernel_size = self.kernel_size
        dilation = self.dilation
        padding_height = (kernel_size[0] - 1) * dilation[0]
        padding_width = (kernel_size[1] - 1) * dilation[1]
        padding_up = padding_height // 2
        padding_bottom = padding_height - padding_up
        padding_left = padding_width // 2
        padding_right = padding_width - padding_left

        x = input

        if self.norm:
            x = self.norm2d(x)
        if self.nonlinear:
            x = self.nonlinear2d(x)
        
        x = F.pad(x, (padding_left, padding_right, padding_up, padding_bottom))
        output = self.conv2d(x)

        return output

def _test_d2block():
    batch_size = 4
    n_bins, n_frames = 16, 64
    in_channels = 3
    kernel_size = (3, 3)
    depth = 4

    input = torch.randn(batch_size, in_channels, n_bins, n_frames)

    print("-"*10, "D2 Block when `growth_rate` is given as int and `dilated` is given as bool.", "-"*10)

    growth_rate = 2
    dilated = True
    model = D2Block(in_channels, growth_rate, kernel_size=kernel_size, dilated=dilated, depth=depth)

    print("-"*10, "D2 Block", "-"*10)
    print(model)
    output = model(input)
    print(input.size(), output.size())
    print()

    print("-"*10, "D2 Block when `growth_rate` is given as list and `dilated` is given as bool.", "-"*10)

    growth_rate = [3, 4, 5, 6] # depth = 4
    dilated = False
    model = D2Block(in_channels, growth_rate, kernel_size=kernel_size, dilated=dilated)

    print(model)
    output = model(input)
    print(input.size(), output.size())
    print()

    print("-"*10, "D2 Block when `growth_rate` is given as list and `dilated` is given as list.", "-"*10)

    growth_rate = [3, 4, 5, 6] # depth = 4
    dilated = [True, False, False, True] # depth = 4
    model = D2Block(in_channels, growth_rate, kernel_size=kernel_size, dilated=dilated)

    print(model)
    output = model(input)
    print(input.size(), output.size())

if __name__ == '__main__':
    torch.manual_seed(111)

    print("="*10, "D2 Block", "="*10)
    _test_d2block()