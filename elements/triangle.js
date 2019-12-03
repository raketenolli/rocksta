// const THREE = require('../three/three');

class Triangle {
    constructor(p0, p1, p2) {
        let triangleWire = new THREE.Geometry();

        this.v0 = new THREE.Vector3(...p0);
        this.v1 = new THREE.Vector3(...p1);
        this.v2 = new THREE.Vector3(...p2);
        triangleWire.vertices.push(this.v0);
        triangleWire.vertices.push(this.v1);
        triangleWire.vertices.push(this.v2);

        this.lineMaterial = new THREE.LineBasicMaterial( { color: 0x0000c0 } );
        this.faceMaterial = new THREE.MeshBasicMaterial( { color: 0xc0c0c0 } );

        this.lines = new THREE.Line(triangleWire, this.lineMaterial);

        let triangleFace = new THREE.BufferGeometry();
        let triangleVertices = new Float32Array([
            ...p0,
            ...p1,
            ...p2
        ]);
        triangleFace.setAttribute("position", new THREE.BufferAttribute(triangleVertices, 3));
        this.face = new THREE.Mesh(triangleFace, this.faceMaterial);

        let d0 = new THREE.Vector3().subVectors(this.v1, this.v0);
        let d1 = new THREE.Vector3().subVectors(this.v2, this.v1);
        this.normal = d0.cross(d1).normalize();
    }

}

// module.exports = Triangle;