#!/usr/bin/env python3
import cherrypy
import os
from models import create_tables, init_sample_data
from web_app import ScholarshipWebApp

def main():
    # Initialize database
    print("Initializing database...")
    create_tables()
    init_sample_data()
    print("Database initialized!")

    # Configure CherryPy
    cherrypy.config.update({
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 8080,
        'engine.autoreload.on': True,
        'log.screen': True
    })

    # Mount the application
    cherrypy.quickstart(ScholarshipWebApp(), '/')

if __name__ == '__main__':
    main()