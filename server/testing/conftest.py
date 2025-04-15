#!/usr/bin/env python3
import pytest
from app import app
from models import db, Plant

@pytest.fixture(scope='module')
def test_client():
    # Configure test database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    
    # Create test client
    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            # Seed test data
            plant = Plant(
                name="Test Plant",
                image="test.jpg",
                price=10.0,
                is_in_stock=True
            )
            db.session.add(plant)
            db.session.commit()
            
            yield testing_client
            
            db.drop_all()
