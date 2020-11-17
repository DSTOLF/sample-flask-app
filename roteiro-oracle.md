
- configurar source oracle
    adicionar environment

    aguardar discovery

    configurar string de conexão ORCLDB
jdbc:oracle:thin:@(DESCRIPTION=(ENABLE=broken)(ADDRESS=(PROTOCOL=tcp)(HOST=oracle-source)(PORT=1521))(CONNECT_DATA=(UR=A)(SID=ORCLCDB)))

    configurar string de conexão VIRTUALCDB
jdbc:oracle:thin:@(DESCRIPTION=(ENABLE=broken)(ADDRESS=(PROTOCOL=tcp)(HOST=oracle-source)(PORT=1521))(CONNECT_DATA=(UR=A)(SID=VIRTUALCDB)))

- conectar ao home oracle
export ORACLE_SID=ORCLCDB
sqlplus / as sysdba
set lines 100 pages 1000
SELECT name, pdb FROM   v$services ORDER BY name;

export ORACLE_SID=VIRTUALCDB
sqlplus / as sysdba
set lines 100 pages 1000
SELECT name, pdb FROM   v$services ORDER BY name;


- configurar vdb BREAKDFIXPDB


- Masking
    Add Application - Flask-App
    Add Environment: mask
        connector: ORCLPDB1
            schema: DELPHIX_DB
            login: DELPHIX_DB
            password: delphix
            JDBC URL
jdbc:oracle:thin:@(DESCRIPTION=(ENABLE=broken)(ADDRESS=(PROTOCOL=tcp)(HOST=oracle-source)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=ORCLPDB1)))

        connector: MASKPDB
            schema: DELPHIX_DB
            login: DELPHIX_DB
            password: delphix
            JDBC URL
jdbc:oracle:thin:@(DESCRIPTION=(ENABLE=broken)(ADDRESS=(PROTOCOL=tcp)(HOST=oracle-source)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=MASKPDB)))

        ruleset: RS_FLASK_APP
            empregado
            empresa
        Profiler: PR_FLASK_APP
            multi tenant: yes

        masking job: MSK_FLASK_APP
            multi tenant: yes

- configurar MASKPDB
    Hooks
        configure: 
            profile-vdb:
                from template
            mask-vdb:
                from template
        
- configurar: DEVPDB

- configurar: QAPDB
