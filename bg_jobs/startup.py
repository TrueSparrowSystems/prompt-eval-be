from graphQL.db_models.evaluation import Evaluation
from bg_jobs.executor import SingletonThreadPoolExecutor
from bg_jobs.background_job import background_job

def startup():
    try:
        evaluations = Evaluation.objects.filter(status__in=['INITIATED', 'FAILED'], retry_count__lt=3).order_by('created_at')
        print('evaluations------',evaluations.count())
        bg_params = []
        for evaluation in evaluations:
            bg_params.append({
                "evaluation_id": evaluation.id,
                "prompt_template_id": evaluation.prompt_template_id
            }) 
        print('bg_params------',bg_params)  
        # bg_params = [
        #     {
        #         "evaluation_id": "1",
        #         "prompt_template_id": "1"
        #     }
        # ]  
        
        if (len(bg_params) > 0):
            executor = SingletonThreadPoolExecutor()
            for bg_param in bg_params:
                print('bg_param------',bg_param)
                executor.submit(background_job, bg_param)

    except Exception as e:
        print("error while startup ------", str(e))
        return e
        
        
            
    
        
 
        

