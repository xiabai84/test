# test

```
  The istio-proxy container has pilot-agent, which can query the local Envoy admin — no istioctl required:

  # dump Envoy config from the app pod's sidecar
  oc exec <app-pod> -c istio-proxy -- pilot-agent request GET config_dump > cd.json

  # find the inbound filter chain for :8800 and whether it requires a client cert (= STRICT)
  python3 - <<'PY'
  import json
  d=json.load(open("cd.json"))
  for c in d.get("configs",[]):
      for l in c.get("dynamic_listeners",[]):
          lis=l.get("active_state",{}).get("listener",{})
          for fc in lis.get("filter_chains",[]):
              if fc.get("filter_chain_match",{}).get("destination_port")==8800:
                  ts=fc.get("transport_socket",{}).get("typed_config",{})
                  print("match:", fc["filter_chain_match"],
                        "| require_client_certificate =", ts.get("require_client_certificate"))
  PY
```
