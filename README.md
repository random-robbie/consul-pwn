# consul-pwn

Make a Consul Agent Grab AWS IAM ROLE keys

This is a little tool to register an agent that will get the IAM role name and then grab the IAM role keys.

Requires Consul Web Interface accessable and settings to allow a new agent.

### How to Run

```
python consul-aws.py -s http://127.0.0.1
```

[![consu.jpg](https://i.postimg.cc/NLhXHv64/consu.jpg)](https://postimg.cc/D4g09DYJ)
