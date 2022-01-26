# __Application landscape : a toy example__

## __Application details__

* __Application name:__ Awesome Analytical Application (AAA)
* __Application components:__ Jobs, APIs, Lib, UI
* __Application services/sub-components:__ ML-Lib, DE-Lib, Application Layer, ML Layer, DE Layer, Utility Layer, ML Jobs, DE Jobs
* __Other components:__ DB, Data Store/Cache, Message broker, Load Balancer/Reverse proxy, Prometheus, Grafana

## __Application components:__

### __Jobs:__

Jobs are some process which can have at least one of the following attributes,

* time taking process
* computation intensive process
* memory consuming process

In addition to the above it has to be stateless. If it gets killed in the process using data, config and code it should be triggered without much hassle.

#### __Details about Jobs in deployment:__

In existing setup jobs can be mainly of two types:

* Celery works
* Independency jobs

A real life example of jobs can be model training, synthetic data generation. In case of model training, if we have a model which is kind of combination of multiple models and each of the models are independent of one another, then the type of job will be different than if it is a single large model. Depending on the model type and the computation behind it and the available orchestration we will have to choose the job accordingly. 

__Celery worker:__ If a job is a celery worker, it will be linked with a message broker (RabbitMQ/Redis) & a backend (Redis or any other DB). Message broker will act as a queue store. If a job is trigger a message will be sent to a queue store. It will be piled in a ordered queue. As and when a job is free/provisioned it will pull a message from queue. Run a job. Change status in Message broker. Write result in backend.


__Independency jobs:__ It can be a python script or a cli app which will run a specific workload. It will be a standalone docker container. One a job is trigger from UI or any other pipeline, a message will be sent in a service bus. This script or job will take up the message from the service bus, run the batch processing task as script or job and write back the result to a DB/storage.

In both the cases, to achieve a truly on-demand auto-scaling infra, we will use KEDA with AKS. Celery works or jobs will be provision, triggered and destroyed depending on the RabbitMQ or Azure Service Bus trigger.

__Notes:__ The schema of auto-scaling and pattern may change depending on the job type.

### __APIs:__

APIs are light weighted stateless process. It will expose some of the functionality in any lib to talk to each other. Other than this it will do other CRUD operations required for the application.

A real life example of APIs can be, lets say you have predicted result on weekly level using a job. Now, you want a aggregated view of the predicted data in a monthly form. Here APIs can be used. Or lets assume that you want to change a existing data for a chart, here this can be helpful.

### __Libs:__ 

Libraries are nothing but collection of packages for a domain of work. For example, in ML code base we have some functionalities which we may want to use in the deployment or share amount users or want to run some experiment on cloud. In that context, here we will bundle all these functionalities in a library and distribute using libraries. Libraries can be created for ML, DE or any other general utils as well.

### __UI:__

As the name suggests this is the frontend application. This will call APIs to show things in browser. Depending on the things needs to be shown in the UI, the application layer APIs will communicate to any other service, get the results and send it back to the UI app.


## __Toy application services/sub-components:__

### __mt-aaa-ml-lib:__

#### __Notes:__

* Centralized ML code base of AAA application.
* Create a library from here & distribute.
* Create a docker base image & distribute.
* Create library, run workload and experiment in cloud.
* User same library in ML Layer for light weight tasks.
* User same library in ML Jobs for batch processing tasks.
* Version control code, version library.
* Test ML code as independent process and then deploy as service.
* This will be a github repository.

#### __Tasks:__

* Train model
* Aggregate results
* generate visualization

### __mt-aaa-ui-app:__

#### __Notes:__

* Standalone UI app containing HTML, CSS and JavaScript code.
* TODO: add additional points here.


#### __Tasks:__

* User login
* Trigger model training
* Check model training status
* Get final model training results
* Get aggregated results
* Visualize aggregated results

### __mt-aaa-be-api:__

#### __Notes:__


* TODO: add additional points here.

#### __Tasks:__

* User login: take info provided in UI, check if DB, if the user is present, send information to UI that the user is valid. Show them the required stuff.
* Submit model training job: When a users, triggers a model run from UI, take that signal, put that in rabbit mq.
* Get model training job status: Check model training results in a DB and show in UI.
* Show model training job results: Once the model training is done, fetch the result from DB/Data store or cache and display the result and send it to the UI.
* Get aggregated results: if a given model id and aggregation level, aggregate the data.
* Visualize aggregated results: given a model id and aggregation, reshape and visualize the data.
* Get all model id & status: get all the models and model status and send it to the UI.


### __mt-aaa-be-job:__

#### __Notes:__


* TODO: add additional points here.

#### __Tasks:__

* Train a model and update the status and results


## Reference:
* https://docs.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-overview?tabs=csharp
* https://arxiv.org/pdf/2103.00033.pdf