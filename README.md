<div align="center">
    <a href="https://www.idurarapp.com/">
  <img src="https://avatars.githubusercontent.com/u/50052356?s=200&v=4" width="128px" />
    </a>
    <h1>Open Source ERP / CRM Accounting Invoice Quote</h1>
    <p align="center">
        <p>IDURAR ERP CRM | Simple To Use</p>
    </p>
    

```
 Give a Star ⭐️ & Fork to this project ... Happy coding! 🤩`
```

IDURAR is Open Source ERP / CRM (Invoice / Quote / Accounting ) Based on Django (Python) with SQLite and React.js with Ant Design (AntD) and Redux

</div>

**🚀 Self-hosted Entreprise Version** : [https://cloud.idurarapp.com](https://cloud.idurarapp.com)


## ⚠️ SECURITY WARNING for Developers & Web Agencies & Blockchain Developer

We’ve been made aware of scammer contacting developers or web agencies, asking them to develop and run malicious or altered versions of IDURAR software.

🚫 NEVER trust emails, messages, or DMs claiming to be from IDURAR unless they come from our official domain: **@idurarapp.com**  
🚫 DO NOT run unknown versions of the app sent via email or third-party GitHub repositories.

✅ Official GitHub Repo: [https://github.com/idurar/idurar-erp-crm](https://github.com/idurar/idurar-erp-crm)  
✅ Official Website: [https://idurarapp.com](https://idurarapp.com)

🚨 WARNING: We have been informed that scammers are misusing this open-source project and falsely claiming to represent IDURAR.AI.

⚠️ Only trust official information, updates, and licenses from our official website: [https://idurarapp.com](https://idurarapp.com). and official github repo: https://github.com/idurar/idurar-erp-crm
We do **not** auhorize any third party to sell, license, or represent our software or brand.

🚫 Never run versions of IDURAR downloaded from unofficial GitHub repositories.  
These may be **fake**, **malicious**, or used to scam users.

✅ Stay safe. Verify the source and always contact us through our website if in doubt.

## Features :

Invoice Management

Payment Management

Quote Management

Customer Management

Ant Design Framework(AntD) 🐜

Based on Mern Stack (Node.js / Express.js / MongoDb / React.js ) 👨‍💻

### May i can use IDURAR for Commercial use :

- Yes You can use IDURAR for free for personal or Commercial use.

## Our Sponsors

  <a href="https://m.do.co/c/4ead8370b905?ref=idurarapp.com">
    <img src="https://opensource.nyc3.cdn.digitaloceanspaces.com/attribution/assets/PoweredByDO/DO_Powered_by_Badge_blue.svg" width="201px">
  </a>

#

<img width="1403" alt="Open Source ERP CRM" src="https://github.com/idurar/idurar-erp-crm/assets/136928179/a6712286-7ca6-4822-8902-fb7523533ee8">

## Free Open Source ERP / CRM App

IDURAR is Open "Fair-Code" Source ERP / CRM (Invoice / Inventory / Accounting / HR) Based on Django (Python) with SQLite and React.js with Ant Design (AntD) and Redux


## Getting started

### Backend

1. Navigate to the Django backend directory:
   ```
   cd django_backend
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```
   python manage.py migrate
   ```

4. Setup initial data:
   ```
   python manage.py setup
   ```

5. Start the server:
   ```
   ./start_server.sh
   ```

The backend will be available at http://localhost:12000/api/

### Frontend

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm run dev -- --port 12001 --host 0.0.0.0
   ```

The frontend will be available at http://localhost:12001/

## Default Admin User

- Email: admin@demo.com
- Password: admin123

## API Endpoints

### Authentication

- `POST /api/login` - Login
- `POST /api/logout` - Logout
- `POST /api/forgetpassword` - Request password reset
- `POST /api/resetpassword` - Reset password

### Clients, Invoices, Quotes, Payments

The API follows a consistent pattern for all entities:

- `POST /api/{entity}/create` - Create entity
- `GET /api/{entity}/read/:id` - Get entity by ID
- `PATCH /api/{entity}/update/:id` - Update entity
- `DELETE /api/{entity}/delete/:id` - Delete entity
- `GET /api/{entity}/list` - Get paginated list of entities
- `GET /api/{entity}/listAll` - Get all entities
- `GET /api/{entity}/filter` - Filter entities
- `GET /api/{entity}/search` - Search entities
- `GET /api/{entity}/summary` - Get entity summary (where applicable)

Where `{entity}` can be: `client`, `invoice`, `quote`, `payment`, `product`, `paymentMode`

## Contributing

1.[How to contribute](https://github.com/idurar/idurar-erp-crm/blob/master/CONTRIBUTING.md#how-to-contribute)

2.[Reporting issues](https://github.com/idurar/idurar-erp-crm/blob/master/CONTRIBUTING.md#reporting-issues)

3.[Working on issues ](https://github.com/idurar/idurar-erp-crm/blob/master/CONTRIBUTING.md#working-on-issues)

4.[Submitting pull requests](https://github.com/idurar/idurar-erp-crm/blob/master/CONTRIBUTING.md#submitting-pull-requests)

5.[Commit Guidelines](https://github.com/idurar/idurar-erp-crm/blob/master/CONTRIBUTING.md#commit-guidelines)

6.[Coding Guidelines](https://github.com/idurar/idurar-erp-crm/blob/master/CONTRIBUTING.md#coding-guidelines)

7.[Questions](https://github.com/idurar/idurar-erp-crm/blob/master/CONTRIBUTING.md#questions)


## Show your support

Dont forget to give a ⭐️ to this project ... Happy coding!

**🚀 Self-hosted Entreprise Version** : [https://cloud.idurarapp.com](https://cloud.idurarapp.com)

## License

IDURAR is Free Open Source Released under the GNU Affero General Public License v3.0.
