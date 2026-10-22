# Requirements Specification

## 1. Purpose of the Service
The microservice is designed for system state monitoring (diagnosing network availability and server time) and providing asynchronous internal order reception via a message broker for subsequent background processing.

## 2. Functional Requirements
*   **R1:** The service must provide the current server time for client synchronization.
*   **R2:** The service must accept diagnostic messages and return them (echo) to verify channel integrity and data parsing.
*   **R3:** The message broker must accept incoming tasks (orders) into a specified topic and store them in memory.
*   **R4:** The broker must serve tasks from the queue upon a consumer (worker) request in strict FIFO (First-In-First-Out) order.

## 3. API Specification (REST & Broker)
Method | Endpoint | Input Data | Output Data | Status Codes | Edge Cases / Errors
---|---|---|---|---|---
GET | `/time` | - | `{"server_time": "string"}` | 200 OK | -
POST | `/echo` | `{"message": "string"}` | `{"message": "string"}` | 200 OK, 400 Bad Request | Returns 400 if the `message` field is missing or the request body is empty.
POST | `/queue/<topic>` | Any JSON object | `{"status": "queued", "topic": "string"}` | 201 Created | Handles empty request bodies (data is saved as an empty object `{}`).
GET | `/queue/<topic>` | - | JSON object from the queue | 200 OK, 204 No Content | Returns 204 if the queue is empty. On status 200, the message is permanently removed from the queue.

## 4. Queue Message Format
Messages sent to the `orders` topic must be in JSON format and describe the attributes of an internal order.
Example structure:
{
  "order_id": 1024,
  "platform": "Wolt",
  "vendor": "Basilic Aksay",
  "timestamp": "2026-10-22T21:10:00Z"
}

## 5. Environment Constraints
*   **Protocol:** Interaction is carried out exclusively via HTTP/1.1 using the application/json data format.
*   **Deployment Environment:** Local execution environment based on Python 3.9+ using the built-in Flask server.
*   **Security:** Data transmission is unencrypted (no HTTPS); authentication is not provided.

## 6. Non-Functional Requirements (NFR)
*   **NFR1 (Latency):** The `/time` and `/echo` endpoints must respond in under 50 ms. *Verification method:* Measuring response time during a local call.
*   **NFR2 (API Fault Tolerance):** The service must not crash when receiving invalid JSON or empty requests. *Verification method:* Sending requests without a Content-Type header and with a missing body (expected safe handling with a 400 or `{}` response).
*   **NFR3 (Asynchrony and Buffering):** The broker must correctly accumulate messages if the consumer is unavailable, without data loss. *Verification method:* Stopping `consumer.py` for 30 seconds while `producer.py` is actively running, followed by resuming the processing of accumulated messages.

## 7. Assumptions
*   **A1 (Environment and Users):** It is assumed that the service operates within an isolated, trusted network. *Link to architecture and risks:* This justifies the omission of authentication and encryption (HTTPS) layers, minimizing development time without a critical risk of data compromise.
*   **A2 (Data Storage):** Loss of undelivered messages upon broker restart is acceptable. *Link to architecture and risks:* An in-memory data structure (a dictionary of lists) is used to implement the broker, ensuring maximum performance (low latency) but carrying the risk of queue clearance if the server process crashes.
*   **A3 (Data Volume):** The size of a single message in the queue does not exceed a few kilobytes, and the sending rate is moderate. *Link to architecture and risks:* The architecture does not include strict limits on the payload size, simplifying the API code under the assumption that there is no risk of out-of-memory (OOM) errors.