deepspeed --num_gpus 2 --num_nodes 1 cli/train.py \
    --output_dir .cache/models \
    --init_ckpt /mnt/scratch/xiayao/cache/pretrained_weights/tinyllama-2-1b \
    --data_path .cache/data/prompt.jsonl \
    --max_seq_len 128 \
    --train_steps 1000 \
    --eval_steps 10 \
    --save_steps 1000 \
    --log_steps 10 \
    --pipe_parallel_size 2 \
    --model_parallel_size 1 \
    --use_flash_attn true \
    --use_fused_ops false \
    --deepspeed_config ./configs/llama.json