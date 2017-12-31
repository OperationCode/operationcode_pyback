
# [OCBotPipeline](https://github.com/OperationCode/operation_code_pybot/ocbot/pipeline)


OCBotPipeline is a module meant direct the primary business logic of slack interactions. This module is meant to be imported by a main web-routing package and have formatted data sent to the primary input. 

## Organization

### To model a pipeline we route in the same behavior

<ol>
    <li>Primary Entrance <code>RoutingHandler</code> takes in <code>event</code></li>
    <li><code>RoutingHandler</code> sends to subclassed <code>RouteHandler</code></li>
    <li><code>RouteHandler</code> performs these actions:</li>
    <ul>
        <li>External: send <code>api_calls</code> get <code>api_resp</code></li>
        <li>Database: send <code>db_calls</code> get <code>db_resp</code></li>
        <li>Incorporate data from <code>[api_resp, event, db_resp]</code> → <code>resp_template</code></li>
        <li>Process <code>resp_template</code> → <code>final_response</code> for approrpriate endpoint</li>
        <li>Combine all <code>final_response</code> objects into <code>List[final_response]</code></li>
         </ul>
    <li>Send <code>List[final_response]</code> to <code>FinalResponseHandler</code></li>  
</ol>


## Create New Route

### New Routing Class

1. Use standard format in one of the <code>pipeline/handlers/abc.py</code> classes to build up your design
2. The class should not perform any direct external calls but rely on other api utilities
3. Create unit tests that verify behavior is correctly performed

### Include new route in Routing Handler
1. Change <code>RoutingHandler</code> so that only these events are directed to this handler.


