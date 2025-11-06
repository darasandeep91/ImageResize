# ImageResize
The goal is to build a multi-stage, backpressured image pipeline that downloads, processes, and saves images concurrently using asyncio primitives, proving mastery of queues, cancellation, timeouts, and graceful shutdown while avoiding event-loop blocking I/O
# Objective
Implement an end-to-end pipeline with distinct async stages—producers enqueue work, downloaders fetch images, processors transform them, and savers persist outputs—where each stage is decoupled by bounded asyncio.Queue to provide flow control and backpressure under load. The system should handle thousands of images with configurable concurrency, rate limiting, and robust shutdown semantics, validating that throughput scales with concurrency without starving or memory bloat
