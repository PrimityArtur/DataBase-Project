
CREATE TABLE USUARIO (
    USUARIO_ID          NUMBER GENERATED ALWAYS AS IDENTITY(START WITH 1 INCREMENT BY 1),
    NOMBRE              VARCHAR2(50) NOT NULL,
    APELLIDO            VARCHAR2(50) NOT NULL,
    CORREO              VARCHAR2(100) NOT NULL UNIQUE,
    CONTRASENA          VARCHAR2(100) NOT NULL,
    FCHA_RGSTRO         DATE DEFAULT SYSDATE NOT NULL,
    
    CONSTRAINT usuario_usuario_id_pk PRIMARY KEY (USUARIO_ID)
);

CREATE TABLE PERFIL (
    USUARIO_ID          NUMBER
        CONSTRAINT perfil_usuario_id_ck UNIQUE,
    PERFIL_ID           NUMBER GENERATED ALWAYS AS IDENTITY(START WITH 1 INCREMENT BY 1),
    FOTO                VARCHAR2(200),
    DIRECCION           VARCHAR2(100),
    TELEFONO            VARCHAR2(20)
        CONSTRAINT perfil_telefono_ck UNIQUE,
    
    CONSTRAINT perfil_id_pk PRIMARY KEY (USUARIO_ID, PERFIL_ID),
    CONSTRAINT perfil_usuario_id_fk FOREIGN KEY (USUARIO_ID) 
        REFERENCES USUARIO(USUARIO_ID) ON DELETE SET NULL
);


CREATE TABLE COMPRADOR (
    COMPRADOR_ID        NUMBER GENERATED ALWAYS AS IDENTITY(START WITH 1 INCREMENT BY 1),
    USUARIO_ID          NUMBER NOT NULL 
    CONSTRAINT comprador_usuario_id_ck UNIQUE,
    
    CONSTRAINT comprador_comprador_id_pk PRIMARY KEY (COMPRADOR_ID),
    CONSTRAINT comprador_usuario_id_fk FOREIGN KEY (USUARIO_ID) 
        REFERENCES USUARIO(USUARIO_ID)
);

CREATE TABLE VENDEDOR (
    USUARIO_ID          NUMBER
        CONSTRAINT vendedor_usuario_id_ck UNIQUE,
    VENDEDOR_ID         NUMBER GENERATED ALWAYS AS IDENTITY(START WITH 1 INCREMENT BY 1),
    
    CONSTRAINT vededor_id_pk PRIMARY KEY (USUARIO_ID, VENDEDOR_ID),
    CONSTRAINT vededor_usuario_id_fk FOREIGN KEY (USUARIO_ID) 
        REFERENCES USUARIO(USUARIO_ID) ON DELETE SET NULL
);

CREATE TABLE ADMINISTRADOR (
    ADMINISTRADOR_ID    NUMBER GENERATED ALWAYS AS IDENTITY(START WITH 1 INCREMENT BY 1),
    USUARIO_ID          NUMBER NOT NULL 
        CONSTRAINT administrador_usuario_id_ck UNIQUE,
    
    CONSTRAINT administrador_administrador_id_pk PRIMARY KEY (ADMINISTRADOR_ID),
    CONSTRAINT administrador_usuario_id_fk FOREIGN KEY (USUARIO_ID) 
        REFERENCES USUARIO(USUARIO_ID)
);

CREATE TABLE PRODUCTO (
    VENDEDOR_ID         NUMBER,
    PRODUCTO_ID         NUMBER GENERATED ALWAYS AS IDENTITY(START WITH 1 INCREMENT BY 1),
    NOMBRE              VARCHAR2(50) NOT NULL,
    DESCRIPCION         VARCHAR2(200) NOT NULL,
    PRECIO              NUMBER(38) NOT NULL
        CONSTRAINT producto_precio_ck CHECK (PRECIO >= 0),
    FECHA               DATE DEFAULT SYSDATE NOT NULL,
    VENDEDOR_USUARIO_ID          NUMBER NOT NULL,
    
    CONSTRAINT producto_id_pk PRIMARY KEY (VENDEDOR_ID, PRODUCTO_ID),
    CONSTRAINT producto_vendedor_fk FOREIGN KEY (VENDEDOR_ID, VENDEDOR_USUARIO_ID) 
        REFERENCES VENDEDOR(VENDEDOR_ID, USUARIO_ID),
    CONSTRAINT producto_precio_min CHECK (PRECIO >= 0)
);

CREATE TABLE TIPO (
    TIPO_ID             NUMBER GENERATED ALWAYS AS IDENTITY(START WITH 1 INCREMENT BY 1),
    VRSION_CMPTBLE      VARCHAR2(50) NOT NULL,
    TIPO                VARCHAR2(10) NOT NULL, --PUGLIN O SCHEMATIC
    PRODUCTO_ID         NUMBER NOT NULL,
    PRODUCTO_VENDEDOR_ID    NUMBER NOT NULL,
    
    CONSTRAINT tipo_tipo_id_pk PRIMARY KEY (TIPO_ID),
    CONSTRAINT tipo_producto_id_fk FOREIGN KEY (PRODUCTO_ID, PRODUCTO_VENDEDOR_ID) 
        REFERENCES PRODUCTO(PRODUCTO_ID, VENDEDOR_ID)
);

CREATE TABLE PLUGIN (
    TIPO_ID             NUMBER,
    VERSION              NUMBER(38) NOT NULL,
    
    CONSTRAINT plugin_tipo_id_pk PRIMARY KEY (TIPO_ID),
    CONSTRAINT plugin_tipo_id_fk FOREIGN KEY (TIPO_ID) 
        REFERENCES TIPO(TIPO_ID) ON DELETE SET NULL
);

CREATE TABLE SCHEMATIC (
    TIPO_ID             NUMBER,
    DIMENSIONES         VARCHAR2(38) NOT NULL,
    
    CONSTRAINT schematic_tipo_id_pk PRIMARY KEY (TIPO_ID),
    CONSTRAINT schematic_tipo_id_fk FOREIGN KEY (TIPO_ID) 
        REFERENCES TIPO(TIPO_ID) ON DELETE SET NULL
);

CREATE TABLE SOPORTE (
    SOPORTE_ID          NUMBER GENERATED ALWAYS AS IDENTITY(START WITH 1 INCREMENT BY 1),
    MENSAJE             VARCHAR2(500) NOT NULL,
    FECHA               DATE DEFAULT SYSDATE NOT NULL,
    USUARIO_ID          NUMBER NOT NULL,
    
    CONSTRAINT soporte_soporte_id_pk PRIMARY KEY (SOPORTE_ID),
    CONSTRAINT soporte_usuario_id_fk FOREIGN KEY (USUARIO_ID) 
        REFERENCES USUARIO(USUARIO_ID)
);

CREATE TABLE RESPUESTA (
    SOPORTE_ID          NUMBER,
    RESPUESTA_ID        NUMBER GENERATED ALWAYS AS IDENTITY(START WITH 1 INCREMENT BY 1),
    MENSAJE             VARCHAR2(500) NOT NULL,
    FECHA               DATE DEFAULT SYSDATE NOT NULL,
    TIPO                VARCHAR2(20) NOT NULL, --USUARIO O ADMINISTRADOR
    USUARIO_ID          NUMBER,
    ADMINISTRADOR_ID    NUMBER,
    
    CONSTRAINT respuesta_id_pk PRIMARY KEY (SOPORTE_ID, RESPUESTA_ID),
    CONSTRAINT respuesta_soporte_id_fk FOREIGN KEY (SOPORTE_ID) 
        REFERENCES SOPORTE(SOPORTE_ID) ON DELETE SET NULL,
    CONSTRAINT respuesta_usuario_id_fk FOREIGN KEY (USUARIO_ID) 
        REFERENCES USUARIO(USUARIO_ID),
    CONSTRAINT respuesta_administrador_id_fk FOREIGN KEY (ADMINISTRADOR_ID) 
        REFERENCES ADMINISTRADOR(ADMINISTRADOR_ID)
);

CREATE TABLE VALORACION (
    COMPRADOR_ID        NUMBER,
    PRODUCTO_ID         NUMBER,
    ESTRELLAS           NUMBER(5) NOT NULL,
    COMENTARIO          VARCHAR2(200) NOT NULL,
    PRODUCTO_VENDEDOR_ID    NUMBER NOT NULL,
    
    CONSTRAINT valoracion_id_pk PRIMARY KEY (COMPRADOR_ID, PRODUCTO_ID),
    CONSTRAINT valoracion_comprador_id_fk FOREIGN KEY (COMPRADOR_ID) 
        REFERENCES COMPRADOR(COMPRADOR_ID) ON DELETE SET NULL,
    CONSTRAINT valoracion_producto_id_fk FOREIGN KEY (PRODUCTO_ID, PRODUCTO_VENDEDOR_ID) 
        REFERENCES PRODUCTO(PRODUCTO_ID, VENDEDOR_ID) ON DELETE SET NULL
);

CREATE TABLE DESCARGA (
    COMPRADOR_ID        NUMBER,
    PRODUCTO_ID         NUMBER,
    FECHA               DATE DEFAULT SYSDATE NOT NULL,
    PRODUCTO_VENDEDOR_ID    NUMBER NOT NULL,
    
    CONSTRAINT descarga_id_pk PRIMARY KEY (COMPRADOR_ID, PRODUCTO_ID),
    CONSTRAINT descarga_comprador_id_fk FOREIGN KEY (COMPRADOR_ID) 
        REFERENCES COMPRADOR(COMPRADOR_ID) ON DELETE SET NULL,
    CONSTRAINT descarga_producto_id_fk FOREIGN KEY (PRODUCTO_ID, PRODUCTO_VENDEDOR_ID) 
        REFERENCES PRODUCTO(PRODUCTO_ID, VENDEDOR_ID) ON DELETE SET NULL
);

CREATE TABLE CARRITO (
    COMPRADOR_ID        NUMBER,
    CARRITO_ID          NUMBER GENERATED ALWAYS AS IDENTITY(START WITH 1 INCREMENT BY 1),
    PRECIO_TOTAL        NUMBER(38) NOT NULL,
    
    CONSTRAINT carrito_id_pk PRIMARY KEY (COMPRADOR_ID, CARRITO_ID),
    CONSTRAINT carrito_comprador_id_fk FOREIGN KEY (COMPRADOR_ID) 
        REFERENCES COMPRADOR(COMPRADOR_ID) ON DELETE SET NULL
);

CREATE TABLE PRDCTO_CRRTO (
    PRDCTO_CRRTO_ID     NUMBER GENERATED ALWAYS AS IDENTITY(START WITH 1 INCREMENT BY 1),
    CANTIDAD            NUMBER(38) NOT NULL
        CONSTRAINT prdcto_cantidad_ck CHECK (CANTIDAD > 0),
    CARRITO_ID          NUMBER NOT NULL,
    PRODUCTO_ID         NUMBER NOT NULL,
    CARRITO_COMPRADOR_ID    NUMBER NOT NULL,
    PRODUCTO_VENDEDOR_ID    NUMBER NOT NULL,
    
    CONSTRAINT prdcto_crrto_id_pk PRIMARY KEY (PRDCTO_CRRTO_ID),
    CONSTRAINT prdcto_crrto_carrito_id_fk FOREIGN KEY (CARRITO_ID, CARRITO_COMPRADOR_ID) 
        REFERENCES CARRITO(CARRITO_ID, COMPRADOR_ID) ON DELETE SET NULL, 
    CONSTRAINT prdcto_crrto_producto_id_fk FOREIGN KEY (PRODUCTO_ID, PRODUCTO_VENDEDOR_ID) 
        REFERENCES PRODUCTO(PRODUCTO_ID, VENDEDOR_ID) ON DELETE SET NULL
);

CREATE TABLE METODO_PAGO (
    METODO_PAGO_ID      NUMBER GENERATED ALWAYS AS IDENTITY(START WITH 1 INCREMENT BY 1),
    NOMBRE              VARCHAR2(50) NOT NULL,
    DESCRIPCION         VARCHAR2(200) NOT NULL,

    CONSTRAINT metodo_pago_metodo_pago_id_pk PRIMARY KEY (METODO_PAGO_ID) 
);


CREATE TABLE PAGO (
    COMPRADOR_ID        NUMBER,
    METODO_PAGO_ID      NUMBER,
    PAGO_ID             NUMBER GENERATED ALWAYS AS IDENTITY(START WITH 1 INCREMENT BY 1),
    FECHA               DATE DEFAULT SYSDATE NOT NULL,
    TOTAL               NUMBER(38) NOT NULL,
    
    CONSTRAINT pago_id_pk PRIMARY KEY (COMPRADOR_ID, METODO_PAGO_ID, PAGO_ID),
    CONSTRAINT pago_comprador_id_fk FOREIGN KEY (COMPRADOR_ID) 
        REFERENCES COMPRADOR(COMPRADOR_ID) ON DELETE SET NULL,   
    CONSTRAINT pago_metodo_pago_id_fk FOREIGN KEY (METODO_PAGO_ID) 
        REFERENCES METODO_PAGO(METODO_PAGO_ID) ON DELETE SET NULL
);

CREATE TABLE RECIBO (
    PAGO_ID             NUMBER 
        CONSTRAINT recibo_pago_id_ck UNIQUE,    
    RECIBO_ID           NUMBER GENERATED ALWAYS AS IDENTITY(START WITH 1 INCREMENT BY 1),
    FECHA               DATE DEFAULT SYSDATE NOT NULL,
    COMPRADOR_ID        NUMBER NOT NULL,
    CARRITO_ID          NUMBER NOT NULL,
    PAGO_COMPRADOR_ID       NUMBER NOT NULL,
    PAGO_METODO_PAGO_ID     NUMBER NOT NULL,
    CARRITO_COMPRADOR_ID    NUMBER NOT NULL,
    
    CONSTRAINT recibo_id_pk PRIMARY KEY (PAGO_ID, RECIBO_ID),
    CONSTRAINT recibo_pago_id_fk FOREIGN KEY (PAGO_ID, PAGO_COMPRADOR_ID, PAGO_METODO_PAGO_ID) 
        REFERENCES PAGO(PAGO_ID, COMPRADOR_ID, METODO_PAGO_ID) ON DELETE SET NULL, 
    CONSTRAINT recibo_comprador_id_fk FOREIGN KEY (COMPRADOR_ID) 
        REFERENCES COMPRADOR(COMPRADOR_ID),    
    CONSTRAINT recibo_carrito_id_fk FOREIGN KEY (CARRITO_ID, CARRITO_COMPRADOR_ID) 
        REFERENCES CARRITO(CARRITO_ID, COMPRADOR_ID)
);


