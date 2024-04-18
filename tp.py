import http.client
import json

def make_post_request(text):
    # Define the server address and endpoint
    server_address = 'localhost:11434'
    endpoint = '/api/generate'
    # Define the payload
    payload = {
        "model": "mistral",
        "prompt": f"Extract and list only the technical skills in the following text:{text} "
    }
    # Convert payload to JSON string
    payload_json = json.dumps(payload)

    try:
        # Create a connection to the server
        connection = http.client.HTTPConnection(server_address)
        # Define request headers
        headers = {'Content-Type': 'application/json'}
        # Send the POST request
        connection.request('POST', endpoint, payload_json, headers)
        # Get the response
        response = connection.getresponse()
        # Print the response status and data
        print("Response status:", response.status)
        print("Response data:")
        response_output = response.read().decode('utf-8').split('\n') 
        json_arr = []
        for i in range(len(response_output)-2):
            json_file = json.loads(response_output[i])
            json_arr.append(json_file)

        output_string = ""
        for json_obj in json_arr:
            output_string+=json_obj["response"]
        print(output_string)
        # Close the connection
        connection.close()
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    text = '''Miko Jr Backend Developer Job Description Company Profile Greetings Miko advanced robotics start headquartered Mumbai company founded January 2015 three IIT Bombay post graduate pillars robotics AI IoT makers Miko series robots designed engage educate entertain kids robots designed diverse team comprising software mechanical engineers mathematicians UI UX designers knowledge partners neuropsychologists India South Korea Russia Growing team 70 professionals 200 channel partners four years ever expanding young energetic organization keen bringing new perspectives experiences insights board mission solve burning consumer problems help robotics AI IoT humanize technology details also visit www miko ai CTC 17 LPA 7 LPA Fixed 6 Lacs Variable 4 Lacs ESOPs Responsibilities Design Development modular reusable backend infrastructure Collaborating cross functional team backend Mobile application AI signal processing Robotics Engineers Design Content Linguistic Team realize requirements conversational social robotics platform Ensure developed backend infrastructure optimized scale responsiveness Ensure best practices design development security monitoring logging DevOps adhere execution project Introducing new ideas products features keeping track latest developments industry trends Skills Proficiency distributed application development lifecycle concepts authentication authorization security session management load balancing API gateway programming techniques tools application tested proven development paradigms Proficiency working Linux based Operating system Proficiency least one server side programming language like Java Additional languages like Python PHP plus Proficiency least one server side framework like Servlets Spring java spark Java Proficiency least one data serialization frameworks Apache Thrift Google ProtoBuffs Apache Avro etc Proficiency least one interprocess communication frameworks WebSockets RPC message queues custom HTTP libraries frameworks kryonet RxJava etc Proficiency multithreaded programming Concurrency concepts Threads Thread Pools Futures asynchronous programming Good understanding networking communication protocols proficiency identifying CPU memory bottlenecks solve read write heavy workloads Proficiency concepts monolithic microservice architectural paradigms Proficiency least one database SQL SQL Graph databases like MySQL MongoDB Orientd Proficiency least one testing frameworks tools Jmeter Locusts Taurus Proficiency least one RPC communication framework Apache Thrift GRPC Proficiency asynchronous libraries RxJava frameworks Akka added plus Proficiency functional programming Scala languages added plus Proficiency working NoSQL graph databases added plus Proficiency working least one cloud hosting platforms like Amazon AWS Google Cloud etc added plus Proficient understanding code versioning tools Git added plus Working Knowledge tools server application metrics logging monitoring plus Monit ELK graylog added plus Working Knowledge DevOps containerization utilities like Ansible Salt Puppet added plus Working Knowledge DevOps containerization technologies like Docker LXD added plus
'''
    make_post_request(text)


