# API Documentation

## AI-Assisted Box Selection System

### Base URL

```
http://127.0.0.1:8000/api/
```

---

# Authentication

This project does not require authentication. All endpoints are publicly accessible for testing purposes.

---

# Product APIs

## Create Product

**Endpoint**

```
POST /api/products/
```

### Request Body

```json
{
    "name": "Wireless Mouse",
    "length": 12,
    "width": 7,
    "height": 4,
    "weight": 0.20
}
```

### Success Response

**201 Created**

```json
{
    "id": 1,
    "name": "Wireless Mouse",
    "length": "12.00",
    "width": "7.00",
    "height": "4.00",
    "weight": "0.20"
}
```

---

## List Products

**Endpoint**

```
GET /api/products/
```

Returns all available products.

---

## Retrieve Product

**Endpoint**

```
GET /api/products/{id}/
```

Example

```
GET /api/products/1/
```

---

## Update Product

**Endpoint**

```
PUT /api/products/{id}/
```

---

## Delete Product

**Endpoint**

```
DELETE /api/products/{id}/
```

**Response**

```
204 No Content
```

---

# Box APIs

## Create Box

**Endpoint**

```
POST /api/boxes/
```

### Request Body

```json
{
    "name": "Medium Box",
    "length": 40,
    "width": 30,
    "height": 20,
    "max_weight": 8
}
```

---

## List Boxes

**Endpoint**

```
GET /api/boxes/
```

---

## Retrieve Box

**Endpoint**

```
GET /api/boxes/{id}/
```

---

## Update Box

**Endpoint**

```
PUT /api/boxes/{id}/
```

---

## Delete Box

**Endpoint**

```
DELETE /api/boxes/{id}/
```

**Response**

```
204 No Content
```

---

# Order APIs

## Create Order

**Endpoint**

```
POST /api/orders/
```

### Request Body

```json
{
    "items": [
        {
            "product": 1,
            "quantity": 2
        },
        {
            "product": 5,
            "quantity": 1
        }
    ]
}
```

### Success Response

```json
{
    "id": 1,
    "status": "Pending",
    "selected_box": null,
    "total_weight": "0.75",
    "items": [
        {
            "id": 1,
            "product": 1,
            "product_name": "Wireless Mouse",
            "quantity": 2
        },
        {
            "id": 2,
            "product": 5,
            "product_name": "Coffee Mug",
            "quantity": 1
        }
    ]
}
```

---

## List Orders

**Endpoint**

```
GET /api/orders/
```

---

## Retrieve Order

**Endpoint**

```
GET /api/orders/{id}/
```

---

## Update Order

**Endpoint**

```
PUT /api/orders/{id}/
```

---

## Delete Order

**Endpoint**

```
DELETE /api/orders/{id}/
```

**Response**

```
204 No Content
```

---

# Box Recommendation API

## Recommend Best Shipping Box

**Endpoint**

```
POST /api/recommend-box/
```

### Request Body

```json
{
    "order_id": 5
}
```

### Success Response

```json
{
    "success": true,
    "order_id": 5,
    "selected_box": "Medium Box",
    "total_weight": "0.75",
    "box_dimensions": {
        "length": "40.00",
        "width": "30.00",
        "height": "20.00"
    },
    "message": "Recommended box selected successfully."
}
```

---

### No Suitable Box Found

```json
{
    "success": false,
    "order_id": 1,
    "selected_box": null,
    "total_weight": "2.95",
    "box_dimensions": null,
    "message": "No suitable box found."
}
```

---

### Empty Order

```json
{
    "success": false,
    "message": "Order does not contain any products."
}
```

---

### Invalid Order

```json
{
    "detail": "Not found."
}
```

---

# Recommendation Algorithm

The recommendation engine follows a simple deterministic packing strategy:

1. Calculate the total weight of all products in the order.
2. Determine the required dimensions:

   * Maximum product length.
   * Maximum product width.
   * Sum of `(product height × quantity)`.
3. Find all boxes that satisfy:

   * Box length ≥ Required length
   * Box width ≥ Required width
   * Box height ≥ Required height
   * Box maximum weight ≥ Total weight
4. Select the smallest suitable box using:

   * Lowest volume
   * Lowest maximum weight (tie-breaker)
   * Alphabetical box name (final tie-breaker)

---

# HTTP Status Codes

| Status Code | Description                         |
| ----------- | ----------------------------------- |
| 200         | Request completed successfully      |
| 201         | Resource created successfully       |
| 204         | Resource deleted successfully       |
| 400         | Invalid request or validation error |
| 404         | Resource not found                  |
| 500         | Internal server error               |

---

# Assumptions

* Each order is packed into a single shipping box.
* Products are stacked vertically when calculating the required height.
* Product rotation is not considered.
* The recommendation algorithm is a simple heuristic and does not implement optimal 3D bin-packing.
* If no box satisfies both dimension and weight constraints, the API returns **"No suitable box found."**

---

# API Endpoints Summary

| Method | Endpoint              | Description                              |
| ------ | --------------------- | ---------------------------------------- |
| GET    | `/api/products/`      | List all products                        |
| POST   | `/api/products/`      | Create a product                         |
| GET    | `/api/products/{id}/` | Retrieve a product                       |
| PUT    | `/api/products/{id}/` | Update a product                         |
| DELETE | `/api/products/{id}/` | Delete a product                         |
| GET    | `/api/boxes/`         | List all boxes                           |
| POST   | `/api/boxes/`         | Create a box                             |
| GET    | `/api/boxes/{id}/`    | Retrieve a box                           |
| PUT    | `/api/boxes/{id}/`    | Update a box                             |
| DELETE | `/api/boxes/{id}/`    | Delete a box                             |
| GET    | `/api/orders/`        | List all orders                          |
| POST   | `/api/orders/`        | Create an order                          |
| GET    | `/api/orders/{id}/`   | Retrieve an order                        |
| PUT    | `/api/orders/{id}/`   | Update an order                          |
| DELETE | `/api/orders/{id}/`   | Delete an order                          |
| POST   | `/api/recommend-box/` | Recommend the most suitable shipping box |
