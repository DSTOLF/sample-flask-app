
- configurar source postgres
    staging mount path /mnt/provision/flask_db
    PostgresDB Replication User: replica
    PostgresDB Replication User Password: delphix

    Source Host Address: 10.0.1.20
    Source Instance Port Number: 5432

    Staging Instance Port Number: 5433
    Config Settings
        listen_addresses *
        max_wal_senders 10
        wal_level hot_standby

- configurar vdb flask_vdb_sust1
    mount path: /mnt/provision/flask_vdb_sust1
    Virtual Postgres Port Number: 5434
    Config Settings
        listen_addresses *
        max_wal_senders 10
        wal_level hot_standby
    Hooks
        configure: 
            start-app:
                /var/lib/pgsql/sample-flask-app/start_flask_app.sh sust
        post-start: 
            start-app:
                /var/lib/pgsql/sample-flask-app/start_flask_app.sh sust
        pre-stop: 
            stop-app:
                /var/lib/pgsql/sample-flask-app/stop_flask_app.sh sust

- Masking
    Add Application - Flask-App
    Add Environment: mask
        connector: flask_sust_vdb1
            schema: public
            database name: flask_db
            host: 10.0.1.30
            port: 5434
            login: delphix
            password: delphix
        ruleset: RS_FLASK_APP
            empregado
            empresa
        Profiler: PR_FLASK_APP
            multi tenant: yes
        Inventory
            exportar
            importar csv no excel
            mostrar dados gerados
        connector: flask_mask_vdb1
            schema: public
            database name: flask_db
            host: 10.0.1.30
            port: 5435
            login: delphix
            password: delphix
        masking job: MSK_FLASK_APP
            pre-script: fk_disable.sql
            post-script: fk_enable.sql

- configurar flask_mask_vdb1
    mount path: /mnt/provision/flask_mask_vdb1
    Virtual Postgres Port Number: 5435
    Config Settings
        listen_addresses *
        max_wal_senders 10
        wal_level hot_standby
    Hooks
        configure: 
            profile-vdb:
                source /var/lib/pgsql/.bash_profile
                cd /var/lib/pgsql/dlpx_masking_script/dxmc
                ./dxmc profilejob start --jobname PR_FLASK_APP --tgt_connector flask_sust_vdb1 --tgt_connector_env mask
            mask-vdb:
                source /var/lib/pgsql/.bash_profile
                cd /var/lib/pgsql/dlpx_masking_script/dxmc
                ./dxmc job start --jobname MSK_FLASK_APP --tgt_connector flask_mask_vdb1 --tgt_connector_env mask
            start-app:
                /var/lib/pgsql/sample-flask-app/start_flask_app.sh msk
        post-start: 
            start-app:
                /var/lib/pgsql/sample-flask-app/start_flask_app.sh msk
        pre-stop: 
            stop-app:
                /var/lib/pgsql/sample-flask-app/stop_flask_app.sh msk
        
- configurar: flask_dev_vdb1
    mount path: /mnt/provision/flask_dev_vdb1
    Virtual Postgres Port Number: 5436
    Config Settings
        listen_addresses *
        max_wal_senders 10
        wal_level hot_standby
    Hooks
        configure: 
            start-app:
                /var/lib/pgsql/sample-flask-app/start_flask_app.sh dev
        post-start: 
            start-app:
                /var/lib/pgsql/sample-flask-app/start_flask_app.sh dev
        pre-stop: 
            stop-app:
                /var/lib/pgsql/sample-flask-app/stop_flask_app.sh dev

- configurar: flask_qa_vdb1
    mount path: /mnt/provision/flaks_qa_vdb1
    Virtual Postgres Port Number: 5437
    Config Settings
        listen_addresses *
        max_wal_senders 10
        wal_level hot_standby
    Hooks:
        configure: 
            start-app:
                /var/lib/pgsql/sample-flask-app/start_flask_app.sh qa
            generate-data:
                /var/lib/pgsql/sample-flask-app/migration_flask_app.sh qa
        post-start: 
            start-app:
                /var/lib/pgsql/sample-flask-app/start_flask_app.sh qa
        pre-stop: 
            stop-app:
                /var/lib/pgsql/sample-flask-app/stop_flask_app.sh qa

- configurar: flask_sint_vdb1
    mount path: /mnt/provision/flask_sint_vdb1
    Virtual Postgres Port Number: 5438
    Config Settings
        listen_addresses *
        max_wal_senders 10
        wal_level hot_standby
    Hooks:
        configure:
            prune-data:
                source /var/lib/pgsql/sample-flask-app/.creds 
                export PGPASSWORD=$DATABASE_PASSWORD
                psql -h 10.0.1.30 -p 5438 -U $DATABASE_USER  -d flask_db -c "delete from empregado where estado!='PR';"
            start-app:
                /var/lib/pgsql/sample-flask-app/start_flask_app.sh sint v2.0
        post-start:
            start-app:
                /var/lib/pgsql/sample-flask-app/start_flask_app.sh sint v2.0
        post-stop:
            stop-app:
                /var/lib/pgsql/sample-flask-app/stop_flask_app.sh sint

    conectar na base:
    create table dependente (id int primary key not null, nome varchar(100), cpf varchar(18), data_nasc date);


Masking: 
    Add Environment: Sintetico
    Profile Job: PR_FLASK_SINT
    Ruleset: 
    tabela dependente
        Custom SQL:
            SELECT "id" , "nome" , "documento_fiscal" as "cpf", date_trunc('day', to_date('2000-01-01', 'yyyy-mm-dd') + (random()*10000 * interval '1 day'))  "data_nasc" FROM "public"."empregado";
    Inventory:
        acrescentar DOB em data_nasc 
            yyyy-mm-dd
    Masking Job: MSK_FLASK_SINT
        on the fly
        source env: mask
        source connector: flask_mask_vdb1
        ore-script: truncate_tables.sql