# ImageResize
The goal is to build a multi-stage, backpressured image pipeline that downloads, processes, and saves images concurrently using asyncio primitives, proving mastery of queues, cancellation, timeouts, and graceful shutdown while avoiding event-loop blocking I/O
# Objective
Implement an end-to-end pipeline with distinct async stages—producers enqueue work, downloaders fetch images, processors transform them, and savers persist outputs—where each stage is decoupled by bounded asyncio.Queue to provide flow control and backpressure under load. The system should handle thousands of images with configurable concurrency, rate limiting, and robust shutdown semantics, validating that throughput scales with concurrency without starving or memory bloat
# Core requirements
Stages and queues: Define at least four stages (URL producer, downloader, processor, saver) connected by bounded asyncio.Queue instances to enforce backpressure and avoid unbounded growth under slow consumers.​

Concurrency control: Use semaphores and per-stage worker counts to cap concurrency; expose knobs for global vs per-host rate limits for fair usage of remote services.​

Async I/O only: Use async-native libs for network and file I/O (e.g., aiohttp and aiofiles) to prevent blocking the event loop; document that asyncio doesn’t provide true async disk I/O on all OSes and a library like aiofiles uses threads under the hood
