import torch
from fmengine.optimizers.loss_func import loss_fn
from transformers.configuration_utils import PretrainedConfig
from fmengine.modeling.llama.llama_model import LlamaModelPipe
from transformers.models.llama.modeling_llama import LlamaConfig
from transformers.models.gpt_neox.modeling_gpt_neox import GPTNeoXConfig
from deepspeed.runtime.pipe.topology import PipeModelDataParallelTopology


def get_model(
        model_config: PretrainedConfig, 
        args, 
        activation_checkpointing_config=None
    ):
    pp = args.pipe_parallel_size
    mp = args.model_parallel_size
    assert args.world_size % (pp * mp) == 0
    dp = args.world_size // (pp * mp)

    topo = PipeModelDataParallelTopology(num_pp=pp, num_mp=mp, num_dp=dp)
    # Offset base seeds for the interior pipeline stages.
    stage_id = topo.get_coord(rank=torch.distributed.get_rank()).pipe
    if 0 < stage_id < topo.get_dim("pipe") - 1:
        args.seed = args.seed + (stage_id * mp)
    if isinstance(model_config, LlamaConfig):
        return LlamaModelPipe(
            model_config,
            loss_fn=loss_fn,
            topology=topo,
            base_seed=args.seed,
            activation_checkpointing_config=activation_checkpointing_config,
        )
    elif isinstance(model_config, GPTNeoXConfig):
        pass
    else:
        raise NotImplementedError