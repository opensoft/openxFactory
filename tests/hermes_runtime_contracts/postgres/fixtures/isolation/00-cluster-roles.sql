\set ON_ERROR_STOP on

DO $roles$
DECLARE
  role_name text;
BEGIN
  FOREACH role_name IN ARRAY ARRAY[
    'hcs_customer_a',
    'hcs_customer_b',
    'hcs_install_admin',
    'hcs_control_plane',
    'hcs_reviewer_a',
    'hcs_reviewer_b',
    'hcs_unbound',
    'hcs_audit'
  ]
  LOOP
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = role_name) THEN
      EXECUTE format(
        'CREATE ROLE %I LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE INHERIT NOREPLICATION NOBYPASSRLS',
        role_name
      );
    END IF;
  END LOOP;
END
$roles$;

GRANT xfactory_v2_runtime TO hcs_customer_a;
GRANT xfactory_v2_runtime TO hcs_customer_b;
GRANT xfactory_v2_runtime TO hcs_install_admin;
GRANT xfactory_v2_runtime TO hcs_reviewer_a;
GRANT xfactory_v2_runtime TO hcs_reviewer_b;
GRANT xfactory_v2_runtime TO hcs_unbound;
GRANT xfactory_v2_control TO hcs_control_plane;
GRANT xfactory_v2_audit TO hcs_audit;

ALTER ROLE hcs_customer_a PASSWORD :'hcs_test_password';
ALTER ROLE hcs_customer_b PASSWORD :'hcs_test_password';
ALTER ROLE hcs_install_admin PASSWORD :'hcs_test_password';
ALTER ROLE hcs_control_plane PASSWORD :'hcs_test_password';
ALTER ROLE hcs_reviewer_a PASSWORD :'hcs_test_password';
ALTER ROLE hcs_reviewer_b PASSWORD :'hcs_test_password';
ALTER ROLE hcs_unbound PASSWORD :'hcs_test_password';
ALTER ROLE hcs_audit PASSWORD :'hcs_test_password';
