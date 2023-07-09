



-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS smartstats.users (
                                                id VARCHAR(25) NOT NULL,
                                                first_name VARCHAR(255) NOT NULL,
                                                last_name VARCHAR(255) NOT NULL,
                                                email VARCHAR(255) NOT NULL,
                                                password VARCHAR(255) NOT NULL,
                                                created_at timestamp NOT NULL,
                                                updated_at timestamp NOT NULL,
                                                date_of_birth DATE NOT NULL,
                                                PRIMARY KEY (id));

ALTER TABLE smartstats.users
    ADD CONSTRAINT check_age CHECK (date_of_birth <= CURRENT_DATE - INTERVAL '18 years'),
    ADD CONSTRAINT check_email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    ADD CONSTRAINT unique_email UNIQUE (email);



-- -----------------------------------------------------
-- Table smartstats.address

-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS smartstats.address (
                                                  id VARCHAR(25) NOT NULL,
                                                  street VARCHAR(255) NOT NULL,
                                                  district_id VARCHAR(25) not null,
                                                  street_num INT NOT NULL,
                                                  apt_num INT NOT NULL,
                                                  zipcode VARCHAR(45) NOT NULL,
                                                  PRIMARY KEY (id),
                                                    foreign key(district_id) references smartstats.districts(id)
                                              on delete cascade
                                              on update cascade);


CREATE TABLE smartstats.districts(
    id VARCHAR(25) not null,
    city VARCHAR(45) NOT NULL,
    district VARCHAR(255) NOT NULL,
                                 primary key(id));
-- -----------------------------------------------------
-- Table smartstats.user_address
set search_path to smartstats;
CREATE TABLE IF NOT EXISTS smartstats.user_address (
                                                       user_id VARCHAR(25) NOT NULL,
                                                       address_id VARCHAR(25) NOT NULL,
                                                       PRIMARY KEY (user_id, address_id),
                                                       FOREIGN KEY (user_id) REFERENCES smartstats.users(id)
                                                   on delete cascade
                                                   on update cascade
);


--
-- CREATE INDEX fk_users_has_address_address1_idx ON smartstats.user_address (address_id ASC) VISIBLE;
--
-- CREATE INDEX fk_users_has_address_users_idx ON smartstats.user_address (user_id ASC) VISIBLE;


-- -----------------------------------------------------
-- Table smartstats.basket
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS smartstats.basket (
                                                 id VARCHAR(25) NOT NULL,
                                                 total_price DOUBLE PRECISION NOT NULL,
                                                 user_id VARCHAR(25) NOT NULL,
                                                 prod_quantity INT NOT NULL,
                                                 PRIMARY KEY (id, user_id),
    foreign key(user_id) references smartstats.users(id)
                                             on delete cascade
                                             on update cascade );

-- CREATE INDEX fk_basket_users1_idx ON smartstats.basket (user_id ASC) VISIBLE;


-- -----------------------------------------------------
-- Table smartstats.products
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS smartstats.products (
                                                   id VARCHAR(25) NOT NULL,
                                                   name VARCHAR(255) NOT NULL,
                                                   brand VARCHAR(45) NOT NULL,
                                                   image_path VARCHAR(255) NOT NULL,
                                                   description VARCHAR(255) NOT NULL,
                                                   store_price INT NOT NULL,
                                                   supplier_price INT NOT NULL,
                                                   PRIMARY KEY (id));


-- -----------------------------------------------------
-- Table smartstats.warehouse
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS smartstats.warehouse (
                                                    id VARCHAR(25) NOT NULL,
                                                    product_id VARCHAR(25) NOT NULL,
                                                    quantity INT NOT NULL,
                                                    PRIMARY KEY (id),
foreign key (product_id) references products(id)
    on delete cascade
       on update cascade);


-- CREATE INDEX fk_warehouse_products1_idx ON smartstats.warehouse (product_id ASC) VISIBLE;


-- -----------------------------------------------------
-- Table smartstats.selected_products
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS smartstats.selected_products (
                                                            product_id VARCHAR(25) NOT NULL,
                                                            basket_id VARCHAR(25) NOT NULL,
                                                            user_id VARCHAR(25) NOT NULL,
                                                            quantity INT NOT NULL,
                                                            price DOUBLE PRECISION,
                                                            PRIMARY KEY (product_id, basket_id, user_id),
                                                                foreign key (product_id) references products(id)

                                                                on delete cascade
                                                                on update cascade,
                                                            foreign key(user_id,basket_id) references basket(user_id, id)
                                                        on delete cascade
                                                        on update cascade);


-- -----------------------------------------------------
-- Table smartstats.orders
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS smartstats.orders (
                                                 id VARCHAR(25) NOT NULL,
                                                 status VARCHAR(45) NULL,
                                                 created_at timestamp NULL,
                                                 updated_at timestamp NULL,
                                                 basket_id VARCHAR(45) NOT NULL,
                                                 user_id VARCHAR(45) NOT NULL,
                                                 PRIMARY KEY (id),
                                                     foreign key (basket_id, user_id) references basket(id, user_id)
                                                     on delete cascade
                                                     on update cascade);

CREATE OR REPLACE FUNCTION update_updated_at()
    RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status IS DISTINCT FROM OLD.status THEN
        NEW.updated_at := NOW();
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_updated_at
    BEFORE UPDATE ON smartstats.orders
    FOR EACH ROW
EXECUTE FUNCTION update_updated_at();


-- CREATE INDEX fk_orders_basket1_idx ON smartstats.orders (basket_id ASC, user_id ASC) VISIBLE;


-- -----------------------------------------------------
-- Table smartstats.categories
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS smartstats.categories (
                                                     id VARCHAR(25) NOT NULL,
                                                     name VARCHAR(255) NOT NULL,
                                                     PRIMARY KEY (id));


-- -----------------------------------------------------
-- Table smartstats.product_categories
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS smartstats.product_categories (
                                                             product_id VARCHAR(25) NOT NULL,
                                                             categories_id VARCHAR(25) NOT NULL,
                                                             PRIMARY KEY (product_id, categories_id),
                                                             foreign key (product_id) references products(id)
                                                                 on delete cascade
                                                                 on update cascade);


CREATE OR REPLACE FUNCTION calculate_price()
    RETURNS TRIGGER AS $$
BEGIN
    NEW.price := NEW.quantity * (
        SELECT store_price
        FROM smartstats.products
        WHERE id = NEW.product_id
    );

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_calculate_price
    BEFORE INSERT ON smartstats.selected_products
    FOR EACH ROW
EXECUTE FUNCTION calculate_price();


CREATE OR REPLACE FUNCTION update_warehouse()
    RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'confirmed' AND OLD.status <> 'confirmed' THEN
        -- Update the warehouse table for all products in selected_products
        UPDATE smartstats.warehouse AS w
        SET quantity = w.quantity - sp.quantity
        FROM smartstats.selected_products AS sp
        WHERE w.product_id = sp.product_id
          AND sp.basket_id = NEW.basket_id
          AND sp.user_id = NEW.user_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_warehouse
    AFTER UPDATE ON smartstats.orders
    FOR EACH ROW
EXECUTE FUNCTION update_warehouse();

CREATE OR REPLACE FUNCTION delete_selected_products()
    RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        DELETE FROM smartstats.selected_products
        WHERE basket_id = NEW.basket_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_delete_selected_products
    AFTER INSERT ON smartstats.orders
    FOR EACH ROW
EXECUTE FUNCTION delete_selected_products();


CREATE OR REPLACE FUNCTION create_default_basket()
    RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO smartstats.basket (id, total_price, user_id, prod_quantity)
    VALUES (NEW.id, 0, NEW.id, 0);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER create_default_basket_trigger
    AFTER INSERT ON smartstats.users
    FOR EACH ROW
EXECUTE FUNCTION create_default_basket();


CREATE OR REPLACE FUNCTION calculate_price()
    RETURNS TRIGGER AS $$
BEGIN
    NEW.price := NEW.quantity * (
        SELECT store_price
        FROM smartstats.products
        WHERE id = NEW.product_id
    );

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION update_basket_total()
    RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        -- Calculate the total quantity and price from selected_products table for insertion
        UPDATE basket
        SET prod_quantity = prod_quantity + NEW.quantity,
            total_price = total_price + NEW.price
        WHERE basket.user_id = NEW.user_id;

    ELSIF (TG_OP = 'DELETE') THEN
        -- Calculate the total quantity and price from selected_products table for deletion
        UPDATE basket
        SET prod_quantity = prod_quantity - OLD.quantity,
            total_price = total_price - OLD.price
        WHERE basket.user_id = OLD.user_id;

    ELSIF (TG_OP = 'UPDATE') THEN
        -- Calculate the total quantity and price from selected_products table for update
        UPDATE basket
        SET prod_quantity = prod_quantity - OLD.quantity + NEW.quantity,
            total_price = total_price - OLD.price + NEW.price
        WHERE basket.user_id = NEW.user_id;

    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger
CREATE TRIGGER update_basket_trigger
    AFTER INSERT OR UPDATE OR DELETE ON selected_products
    FOR EACH ROW
EXECUTE FUNCTION update_basket_total();