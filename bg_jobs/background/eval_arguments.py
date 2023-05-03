
class EvalArguments:
    def __init__(self, **kwargs):
      print(" **kwargs ---- \n", kwargs)
      
      self.completion_fn = kwargs.get('completion_fn', '')
      self.eval = kwargs.get('eval', '')
      self.extra_eval_params = kwargs.get('extra_eval_params', '')
      self.max_samples = kwargs.get('max_samples', '')
      self.cache = kwargs.get('cache', True)
      self.visible = kwargs.get('visible', '')
      self.seed = kwargs.get('seed', '')
      self.user = kwargs.get('user', '')
      self.record_path = kwargs.get('record_path', '')
      self.log_to_file = kwargs.get('log_to_file', '')
      self.registry_path = kwargs.get('registry_path', '')
      if not self.registry_path:
          self.registry_path = kwargs.get('registry_path', [])
      self.debug = kwargs.get('debug', '')
      self.local_run = kwargs.get('local_run', '')
      self.dry_run = kwargs.get('dry_run', '')
      self.dry_run_logging = kwargs.get('dry_run_logging', True)
