class Cylinder {
    constructor(front, end, radius, numberOfSegmentsLengthwise, numberOfSegmentsCircumferential) {
        this.triangles = [];
        this.axis = new THREE.Vector3().subVectors(front, end);
        this.lengthSegment = this.axis.clone().multiplyScalar(-1.0 / numberOfSegmentsLengthwise);
        
        for(let l = 0; l < numberOfSegmentsLengthwise; l++) {
            let segmentFront = front
                .clone()
                .add(this.lengthSegment.clone().multiplyScalar(l));
            console.log(`segmentFront: ${JSON.stringify(segmentFront)}`);
            let segmentEnd = front
                .clone()
                .add(this.lengthSegment.clone().multiplyScalar(l + 1));
            console.log(`segmentEnd: ${JSON.stringify(segmentEnd)}`);
            for(let c = 0; c < numberOfSegmentsCircumferential; c++) {
                console.log(`c: ${c}`);
                let segmentRadius1 = radius
                    .clone()
                    .applyAxisAngle(
                        this.axis.clone().normalize(), 
                        c / numberOfSegmentsCircumferential * 2 * Math.PI
                    );
                console.log(`segmentRadius1: ${JSON.stringify(segmentRadius1)}`);
                let segmentRadius2 = radius
                    .clone()
                    .applyAxisAngle(
                        this.axis.clone().normalize(), 
                        (c + 1) / numberOfSegmentsCircumferential * 2 * Math.PI
                    );
                console.log(`segmentRadius2: ${JSON.stringify(segmentRadius2)}`);
                let p0 = segmentFront.clone().add(segmentRadius1);
                let p1 = segmentEnd.clone().add(segmentRadius1);
                let p2 = segmentEnd.clone().add(segmentRadius2);
                this.triangles.push(new Triangle(
                    p0.toArray(),
                    p1.toArray(),
                    p2.toArray()
                ));
                let p3 = segmentFront.clone().add(segmentRadius1);
                let p4 = segmentEnd.clone().add(segmentRadius2);
                let p5 = segmentFront.clone().add(segmentRadius2);
                this.triangles.push(new Triangle(
                    p3.toArray(),
                    p4.toArray(),
                    p5.toArray()
                ));
            }
        }

        this.lines = this.triangles.map(t => t.lines);
        this.faces = this.triangles.map(t => t.face);
    }
}